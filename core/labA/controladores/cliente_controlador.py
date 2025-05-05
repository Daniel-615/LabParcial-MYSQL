from flask import jsonify, request

class Cliente:
    def __init__(self, db, models, sede):
        self.db = db
        self.models = models
        self.sede = sede

    def _get_model(self):
        return {
            'salvador': self.models.CLIENTE_SV,
            'mexico': self.models.CLIENTE_MX
        }.get(self.sede, None)

    def get_clientes(self):
        try:
            Model = self._get_model()
            if not Model:
                return jsonify({'message': 'Sede inválida'}), 400

            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            clientes = Model.query.order_by(Model.nombre).paginate(
                page=page, per_page=per_page, error_out=False
            )

            if not clientes.items:
                return jsonify({'message': 'No hay clientes registrados'}), 404

            return jsonify({
                'clientes': [cliente.to_dict() for cliente in clientes.items],
                'total': clientes.total,
                'pagina_actual': clientes.page,
                'total_paginas': clientes.pages
            }), 200

        except Exception as e:
            print("Error en get_clientes:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def get_cliente_by_id(self, id):
        try:
            Model = self._get_model()
            if not Model:
                return jsonify({'message': 'Sede inválida'}), 400

            cliente = Model.query.filter_by(id=id).first()

            if not cliente:
                return jsonify({'message': 'Cliente no encontrado'}), 404

            return jsonify(cliente.to_dict()), 200

        except Exception as e:
            print("Error en get_cliente_by_id:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def create_cliente(self, json_data):
        try:
            Model = self._get_model()
            if not Model:
                return jsonify({'message': 'Sede inválida'}), 400

            nombre = json_data.get('nombre')
            direccion = json_data.get('direccion')
            telefono = json_data.get('telefono')
            email = json_data.get('email')

            if not nombre or not direccion or not telefono or not email:
                return jsonify({'message': "'nombre', 'direccion', 'telefono' y 'email' son requeridos"}), 400

            nuevo_cliente = Model(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                email=email
            )
            self.db.session.add(nuevo_cliente)
            self.db.session.commit()

            return jsonify({
                'message': 'Cliente creado',
                'cliente': nuevo_cliente.to_dict()
            }), 201

        except Exception as e:
            print("Error en create_cliente:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def update_cliente(self, id, json_data):
        try:
            Model = self._get_model()
            if not Model:
                return jsonify({'message': 'Sede inválida'}), 400

            cliente = Model.query.filter_by(id=id).first()
            if not cliente:
                return jsonify({'message': 'Cliente no encontrado'}), 404

            if 'nombre' in json_data:
                cliente.nombre = json_data['nombre']
            if 'direccion' in json_data:
                cliente.direccion = json_data['direccion']
            if 'telefono' in json_data:
                cliente.telefono = json_data['telefono']
            if 'email' in json_data:
                cliente.email = json_data['email']

            self.db.session.commit()

            return jsonify({
                'message': 'Cliente actualizado',
                'cliente': cliente.to_dict()
            }), 200

        except Exception as e:
            print("Error en update_cliente:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500