from flask import request

class Incidencia:
    def __init__(self, app, app_initializer, sede):
        self.app = app
        self.app_initializer = app_initializer
        self.sede = sede
        self.routes()

    def routes(self):
        base_path = f'/api/mysql/{self.sede}/incidencia'

        @self.app.route(f'{base_path}', methods=['GET'], endpoint=f'get_incidencias_{self.sede}')
        def get_incidencias():
            return self.app_initializer.getIncidenciaController(self.sede).get_incidencias()

        @self.app.route(f'{base_path}/<int:id>', methods=['GET'], endpoint=f'get_incidencia_by_id_{self.sede}')
        def get_incidencia_by_id(id):
            return self.app_initializer.getIncidenciaController(self.sede).get_incidencia_by_id(id)

        @self.app.route(f'{base_path}', methods=['POST'], endpoint=f'create_incidencia_{self.sede}')
        def create_incidencia():
            return self.app_initializer.getIncidenciaController(self.sede).create_incidencia(request.json)

        @self.app.route(f'{base_path}/<int:id>', methods=['PUT'], endpoint=f'update_incidencia_{self.sede}')
        def update_incidencia(id):
            return self.app_initializer.getIncidenciaController(self.sede).update_incidencia(id, request.json)