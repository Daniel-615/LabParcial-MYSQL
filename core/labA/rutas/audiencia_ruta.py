from flask import request

class Audiencia:
    def __init__(self, app, app_initializer, sede):
        self.app = app
        self.app_initializer = app_initializer
        self.sede = sede
        self.routes()

    def routes(self):
        base_path = f'/api/mysql/{self.sede}/audiencia'

        @self.app.route(f'{base_path}', methods=['GET'], endpoint=f'get_audiencia_{self.sede}')
        def get_audiencia():
            return self.app_initializer.getAudienciaController(self.sede).get_all_audiencias()

        @self.app.route(f'{base_path}/<int:id>', methods=['GET'], endpoint=f'get_audiencia_by_id_{self.sede}')
        def get_audiencia_by_id(id):
            return self.app_initializer.getAudienciaController(self.sede).get_audiencia_by_id(id)

        @self.app.route(f'{base_path}', methods=['POST'], endpoint=f'create_audiencia_{self.sede}')
        def create_audiencia():
            return self.app_initializer.getAudienciaController(self.sede).create_audiencia(request.json,self.sede)

        @self.app.route(f'{base_path}/<int:id>', methods=['PUT'], endpoint=f'update_audiencia_{self.sede}')
        def update_audiencia(id):
            return self.app_initializer.getAudienciaController(self.sede).update_audiencia(id, request.json,self.sede)