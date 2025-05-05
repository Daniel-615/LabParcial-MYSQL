from flask import request, jsonify

class Abogado:
    def __init__(self, db, models, sede):
        self.db = db
        self.models = models
        self.sede = sede 

    def get_abogado(self):
        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            query = self.db.session.query(self.models.ABOGADO[self.sede])
            abogados = query.order_by(self.models.ABOGADO[self.sede].nombre).paginate(
                page=page, per_page=per_page, error_out=False
            )

            if not abogados.items:
                return jsonify({'message': 'No hay abogados registrados'}), 404

            return jsonify({
                "abogados": [a.to_dict() for a in abogados.items],
                "total": abogados.total,
                "pagina_actual": abogados.page,
                "total_paginas": abogados.pages,
            }), 200

        except Exception as e:
            print("Error en get_abogado:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def get_abogado_by_id(self, dni):
        try:
            abogado = self.db.session.query(self.models.ABOGADO[self.sede]).filter_by(dni=dni).first()
            if not abogado:
                return jsonify({'message': 'Abogado no encontrado'}), 404

            return jsonify(abogado.to_dict()), 200

        except Exception as e:
            print("Error en get_abogado_by_id:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def create_abogado(self, json_abogado):
        try:
            dni = json_abogado.get('dni')
            nombre = json_abogado.get('nombre')
            gabinete_id = json_abogado.get('gabinete_id')

            if not dni or not nombre or gabinete_id is None:
                return jsonify({'message': "'dni', 'nombre' y 'gabinete_id' son obligatorios"}), 400

            # Verificar si ya existe el abogado
            if self.db.session.query(self.models.ABOGADO[self.sede]).filter_by(dni=dni).first():
                return jsonify({'message': 'Ya existe un abogado con ese dni'}), 409

            # Verificar que el gabinete exista
            gabinete = self.db.session.query(self.models.GABINETE[self.sede]).filter_by(id=gabinete_id).first()
            if not gabinete:
                return jsonify({'message': 'Gabinete no encontrado'}), 404

            nuevo_abogado = self.models.ABOGADO[self.sede](
                dni=dni,
                nombre=nombre,
                gabinete_id=gabinete_id
            )

            self.db.session.add(nuevo_abogado)
            self.db.session.commit()

            return jsonify({
                "message": "Abogado creado correctamente",
                "abogado": nuevo_abogado.to_dict()
            }), 201

        except Exception as e:
            print("Error en create_abogado:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def update_abogado(self, dni, json_abogado):
        try:
            abogado = self.db.session.query(self.models.ABOGADO[self.sede]).filter_by(dni=dni).first()
            if not abogado:
                return jsonify({'message': 'Abogado no encontrado'}), 404

            nuevo_nombre = json_abogado.get('nombre')
            nuevo_gabinete_id = json_abogado.get('gabinete_id')

            cambios = []

            if nuevo_nombre:
                abogado.nombre = nuevo_nombre
                cambios.append('nombre')

            if nuevo_gabinete_id is not None:
                gabinete = self.db.session.query(self.models.GABINETE[self.sede]).filter_by(id=nuevo_gabinete_id).first()
                if not gabinete:
                    return jsonify({'message': 'Gabinete no encontrado'}), 404
                abogado.gabinete_id = nuevo_gabinete_id
                cambios.append('gabinete_id')

            if not cambios:
                return jsonify({'message': 'No se realizaron cambios'}), 400

            self.db.session.commit()
            return jsonify({
                "message": f"Abogado actualizado correctamente ({', '.join(cambios)})",
                "abogado": abogado.to_dict()
            }), 200

        except Exception as e:
            print("Error en update_abogado:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500
