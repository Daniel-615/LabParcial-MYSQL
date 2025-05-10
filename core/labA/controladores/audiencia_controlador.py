from flask import request, jsonify
from datetime import datetime
import requests

class Audiencia:
    def __init__(self, db, models, sede):
        self.db = db
        self.models = models
        self.sede = sede

    def _get_model(self, sede):
        return self.models.AUDIENCIA.get(sede), self.models.ASUNTO.get(sede), self.models.ABOGADO.get(sede)

    def _validar_fecha(self, fecha_str):
        try:
            return datetime.fromisoformat(fecha_str.replace(" ", "T"))
        except (ValueError, TypeError):
            return None

    def get_all_audiencias(self, sede):
        try:
            AudienciaModel, _, _ = self._get_model(sede)

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            audiencias = AudienciaModel.query.order_by(AudienciaModel.fecha).paginate(
                page=page, per_page=per_page, error_out=False
            )

            if not audiencias.items:
                return jsonify({'message': 'No hay audiencias registradas'}), 404

            return jsonify({
                'audiencias': [a.to_dict() for a in audiencias.items],
                'total': audiencias.total,
                'pagina_actual': audiencias.page,
                'total_paginas': audiencias.pages
            }), 200

        except Exception as e:
            print("Error en get_all_audiencias:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def get_audiencia_by_id(self, id, sede):
        try:
            AudienciaModel, _, _ = self._get_model(sede)

            audiencia = AudienciaModel.query.get(id)
            if not audiencia:
                return jsonify({'message': 'Audiencia no encontrada'}), 404

            return jsonify({'audiencia': audiencia.to_dict()}), 200

        except Exception as e:
            print("Error en get_audiencia_by_id:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def create_audiencia(self, json_data, sede):
        try:
            AudienciaModel, AsuntoModel, AbogadoModel = self._get_model(sede)

            asunto_exp = json_data.get('asunto_exp')
            fecha_str = json_data.get('fecha')
            abogado_dni = json_data.get('abogado_dni')

            if not asunto_exp or not fecha_str or not abogado_dni:
                return jsonify({'message': 'Campos obligatorios: asunto_exp, fecha, abogado_dni'}), 400

            fecha = self._validar_fecha(fecha_str)
            if not fecha:
                return jsonify({'message': 'Formato de fecha inválido. Usa ISO 8601'}), 400

            asunto = AsuntoModel.query.filter_by(expediente=asunto_exp).first()
            abogado = AbogadoModel.query.filter_by(dni=abogado_dni).first()

            if not asunto:
                return jsonify({'message': 'Asunto no encontrado'}), 404
            if not abogado:
                return jsonify({'message': 'Abogado no encontrado'}), 404

            nueva_audiencia = AudienciaModel(
                asunto_exp=asunto_exp,
                fecha=fecha,
                abogado_dni=abogado_dni
            )

            self.db.session.add(nueva_audiencia)
            self.db.session.commit()

            try:
                requests.post('http://localhost:5000/api/oracle/log_asunto', json={
                    'expediente': asunto_exp,
                    'accion': f'AUDIENCIA CREADA {nueva_audiencia.id}'
                })
            except Exception as log_err:
                print(f' No se pudo replicar a Oracle: {log_err}')

            return jsonify({'audiencia': nueva_audiencia.to_dict()}), 201

        except Exception as e:
            print("Error en create_audiencia:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def update_audiencia(self, id, json_data, sede):
        try:
            AudienciaModel, _, AbogadoModel = self._get_model(sede)

            audiencia = AudienciaModel.query.get(id)
            if not audiencia:
                return jsonify({'message': 'Audiencia no encontrada'}), 404

            cambios = []

            if 'fecha' in json_data:
                fecha = self._validar_fecha(json_data['fecha'])
                if not fecha:
                    return jsonify({'message': 'Formato de fecha inválido. Usa ISO 8601'}), 400
                audiencia.fecha = fecha
                cambios.append('fecha')

            if 'abogado_dni' in json_data:
                abogado = AbogadoModel.query.filter_by(dni=json_data['abogado_dni']).first()
                if not abogado:
                    return jsonify({'message': 'Abogado no encontrado'}), 404
                audiencia.abogado_dni = abogado.dni
                cambios.append('abogado_dni')

            self.db.session.commit()

            try:
                requests.post('http://localhost:5000/api/oracle/log_asunto', json={
                    'expediente': audiencia.asunto_exp,
                    'accion': f'AUDIENCIA ACTUALIZADA {id} | CAMBIOS: {", ".join(cambios)}'
                })
            except Exception as log_err:
                print(f'No se pudo replicar a Oracle: {log_err}')

            return jsonify({'audiencia': audiencia.to_dict()}), 200

        except Exception as e:
            print("Error en update_audiencia:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500
