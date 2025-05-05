from flask import jsonify, request

class Incidencia:
    def __init__(self, db, models,sede):
        self.db = db
        self.models = models
        self.sede=sede

    def _get_model(self, sede):
        return {
            'salvador': (self.models.INCIDENCIA_SV, self.models.AUDIENCIA_SV),
            'mexico': (self.models.INCIDENCIA_MX, self.models.AUDIENCIA_MX)
        }.get(sede, (None, None))

    def get_incidencias(self, sede):
        try:
            IncidenciaModel, _ = self._get_model(sede)
            if not IncidenciaModel:
                return jsonify({'message': 'Sede inválida'}), 400

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            incidencias = IncidenciaModel.query.order_by(IncidenciaModel.descripcion).paginate(
                page=page, per_page=per_page, error_out=False)

            if not incidencias.items:
                return jsonify({'message': 'No hay incidencias registradas'}), 404

            return jsonify({
                'incidencias': [i.to_dict() for i in incidencias.items],
                'total': incidencias.total,
                'pagina_actual': incidencias.page,
                'total_paginas': incidencias.pages
            }), 200

        except Exception as e:
            print("Error en get_incidencias:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def get_incidencia_by_id(self, sede, id):
        try:
            IncidenciaModel, _ = self._get_model(sede)
            if not IncidenciaModel:
                return jsonify({'message': 'Sede inválida'}), 400

            incidencia = IncidenciaModel.query.filter_by(id=id).first()

            if not incidencia:
                return jsonify({'message': 'Incidencia no encontrada'}), 404

            return jsonify(incidencia.to_dict()), 200

        except Exception as e:
            print("Error en get_incidencia_by_id:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def create_incidencia(self, sede, json_data):
        try:
            IncidenciaModel, AudienciaModel = self._get_model(sede)
            if not IncidenciaModel or not AudienciaModel:
                return jsonify({'message': 'Sede inválida'}), 400

            audiencia_id = json_data.get('audiencia_id')
            descripcion = json_data.get('descripcion')

            if not audiencia_id or not descripcion:
                return jsonify({'message': "'audiencia_id' y 'descripcion' son requeridos"}), 400

            audiencia = AudienciaModel.query.filter_by(id=audiencia_id).first()
            if not audiencia:
                return jsonify({'message': 'Audiencia no encontrada'}), 404

            nueva_incidencia = IncidenciaModel(
                audiencia_id=audiencia_id,
                descripcion=descripcion
            )
            self.db.session.add(nueva_incidencia)
            self.db.session.commit()

            return jsonify({
                'message': 'Incidencia creada',
                'incidencia': nueva_incidencia.to_dict()
            }), 201

        except Exception as e:
            print("Error en create_incidencia:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def update_incidencia(self, sede, id, json_data):
        try:
            IncidenciaModel, _ = self._get_model(sede)
            if not IncidenciaModel:
                return jsonify({'message': 'Sede inválida'}), 400

            incidencia = IncidenciaModel.query.filter_by(id=id).first()

            if not incidencia:
                return jsonify({'message': 'Incidencia no encontrada'}), 404

            descripcion = json_data.get('descripcion')
            if descripcion:
                incidencia.descripcion = descripcion

            self.db.session.commit()

            return jsonify({
                'message': 'Incidencia actualizada',
                'incidencia': incidencia.to_dict()
            }), 200

        except Exception as e:
            print("Error en update_incidencia:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500