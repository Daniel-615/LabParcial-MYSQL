from flask import request

class Gabinete:
    def __init__(self, app, app_initializer, sede):
        self.app = app
        self.app_initializer = app_initializer
        self.sede = sede
        self.routes()

    def routes(self):
        base_path = f'/api/mysql/{self.sede}/gabinete'

        @self.app.route(f'{base_path}', methods=['GET'], endpoint=f'get_gabinetes_{self.sede}')
        def get_gabinetes():
            return self.app_initializer.getGabineteController(self.sede).get_gabinetes()

        @self.app.route(f'{base_path}/<int:id>', methods=['GET'], endpoint=f'get_gabinete_by_id_{self.sede}')
        def get_gabinete_by_id(id):
            return self.app_initializer.getGabineteController(self.sede).get_gabinete_by_id(id)

        @self.app.route(f'{base_path}', methods=['POST'], endpoint=f'create_gabinete_{self.sede}')
        def create_gabinete():
            return self.app_initializer.getGabineteController(self.sede).create_gabinete(self.sede,request.json)

        @self.app.route(f'{base_path}/<int:id>', methods=['PUT'], endpoint=f'update_gabinete_{self.sede}')
        def update_gabinete(id):
            return self.app_initializer.getGabineteController(self.sede).update_gabinete(id, request.json)