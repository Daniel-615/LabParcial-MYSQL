from flask import request

class Cliente:
    def __init__(self, app, app_initializer, sede):
        self.app = app
        self.app_initializer = app_initializer
        self.sede = sede
        self.routes()

    def routes(self):
        base_path = f'/api/mysql/{self.sede}/cliente'

        @self.app.route(f'{base_path}', methods=['GET'], endpoint=f'get_clientes_{self.sede}')
        def get_clientes():
            return self.app_initializer.getClienteController(self.sede).get_clientes()

        @self.app.route(f'{base_path}/<int:id>', methods=['GET'], endpoint=f'get_cliente_by_id_{self.sede}')
        def get_cliente_by_id(id):
            return self.app_initializer.getClienteController(self.sede).get_cliente_by_id(id)

        @self.app.route(f'{base_path}', methods=['POST'], endpoint=f'create_cliente_{self.sede}')
        def create_cliente():
            return self.app_initializer.getClienteController(self.sede).create_cliente(request.json)

        @self.app.route(f'{base_path}/<int:id>', methods=['PUT'], endpoint=f'update_cliente_{self.sede}')
        def update_cliente(id):
            return self.app_initializer.getClienteController(self.sede).update_cliente(id, request.json)