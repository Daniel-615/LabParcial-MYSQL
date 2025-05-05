from flask import jsonify, request

class Gabinete:
    def __init__(self, db, models,sede):
        self.db = db
        self.models = models
        self.sede=sede

    def _get_model(self, sede):
        try:
            return {
                'salvador': self.models.GABINETE_SV,
                'mexico': self.models.GABINETE_MX
            }.get(self.sede,None)
        except KeyError:
            return None

    def get_gabinetes(self, sede):
        try:
            Model = self._get_model(sede)
            if not Model:
                return jsonify({'message': 'Sede inválida'}), 400

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            gabinetes = Model.query.order_by(Model.nombre).paginate(
                page=page, per_page=per_page, error_out=False
            )

            if not gabinetes.items:
                return jsonify({'message': 'No hay gabinetes registrados'}), 404

            return jsonify({
                'gabinetes': [g.to_dict() for g in gabinetes.items],
                'total': gabinetes.total,
                'pagina_actual': gabinetes.page,
                'total_paginas': gabinetes.pages
            }), 200

        except Exception as e:
            print("Error en get_gabinetes:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def get_gabinete_by_id(self, sede, id):
        try:
            Model = self._get_model(sede)
            if not Model:
                return jsonify({'message': 'Sede inválida'}), 400

            gabinete = Model.query.filter_by(id=id).first()
            if not gabinete:
                return jsonify({'message': 'Gabinete no encontrado'}), 404

            return jsonify(gabinete.to_dict()), 200

        except Exception as e:
            print("Error en get_gabinete_by_id:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def create_gabinete(self, sede, json_data):
        try:
            Model = self._get_model(sede)
            if not Model:
                return jsonify({'message': 'Sede inválida'}), 400

            nombre = json_data.get('nombre')
            pais = json_data.get('pais')
            sistema_operativo = json_data.get('sistema_operativo')

            if not all([nombre, pais, sistema_operativo]):
                return jsonify({'message': "'nombre', 'pais' y 'sistema_operativo' son requeridos"}), 400

            nuevo_gabinete = Model(
                nombre=nombre,
                pais=pais,
                sistema_operativo=sistema_operativo
            )
            self.db.session.add(nuevo_gabinete)
            self.db.session.commit()

            return jsonify({
                'message': 'Gabinete creado',
                'gabinete': nuevo_gabinete.to_dict()
            }), 201

        except Exception as e:
            print("Error en create_gabinete:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def update_gabinete(self, sede, id, json_data):
        try:
            Model = self._get_model(sede)
            if not Model:
                return jsonify({'message': 'Sede inválida'}), 400

            gabinete = Model.query.filter_by(id=id).first()
            if not gabinete:
                return jsonify({'message': 'Gabinete no encontrado'}), 404

            if 'nombre' in json_data:
                gabinete.nombre = json_data['nombre']
            if 'pais' in json_data:
                gabinete.pais = json_data['pais']
            if 'sistema_operativo' in json_data:
                gabinete.sistema_operativo = json_data['sistema_operativo']

            self.db.session.commit()

            return jsonify({
                'message': 'Gabinete actualizado',
                'gabinete': gabinete.to_dict()
            }), 200

        except Exception as e:
            print("Error en update_gabinete:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500