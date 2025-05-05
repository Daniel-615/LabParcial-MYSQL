from flask import request

class Abogado:
    def __init__(self, app, app_initializer, sede):
        self.app = app
        self.app_initializer = app_initializer
        self.sede = sede
        self.routes()

    def routes(self):
        base_path = f'/api/mysql/{self.sede}/abogado'

        @self.app.route(f'{base_path}', methods=['GET'], endpoint=f'get_abogado_{self.sede}')
        def get_abogado():
            return self.app_initializer.getAbogadoController(self.sede).get_abogado()

        @self.app.route(f'{base_path}/<string:dni>', methods=['GET'], endpoint=f'get_abogado_by_id_{self.sede}')
        def get_abogado_by_id(dni):
            return self.app_initializer.getAbogadoController(self.sede).get_abogado_by_id(dni)

        @self.app.route(f'{base_path}', methods=['POST'], endpoint=f'create_abogado_{self.sede}')
        def create_abogado():
            return self.app_initializer.getAbogadoController(self.sede).create_abogado(request.json)

        @self.app.route(f'{base_path}/<string:dni>', methods=['PUT'], endpoint=f'update_abogado_{self.sede}')
        def update_abogado(dni):
            return self.app_initializer.getAbogadoController(self.sede).update_abogado(dni, request.json)