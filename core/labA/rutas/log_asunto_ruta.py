from flask import request

class LogAsunto:
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        @self.app.route('/api/oracle/guatemala/log_asunto', methods=['GET'])
        def get_logs():
            return self.app_initializer.getLogAsuntoController().get_logs()

        @self.app.route('/api/oracle/log_asunto/<int:id>', methods=['GET'])
        def get_log_by_id(id):
            return self.app_initializer.getLogAsuntoController().get_log_by_id(id)

        @self.app.route('/api/oracle/log_asunto', methods=['POST'])
        def create_log():
            return self.app_initializer.getLogAsuntoController().create_log(request.json)

        @self.app.route('/api/oracle/log_asunto/<int:id>', methods=['PUT'])
        def update_log(id):
            return self.app_initializer.getLogAsuntoController().update_log(id, request.json)

        @self.app.route('/api/oracle/inner_join/log_asunto', methods=['GET'])
        def inner_join():
            return self.app_initializer.getLogAsuntoController().innerJoin()
