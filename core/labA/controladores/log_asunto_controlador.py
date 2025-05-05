from flask import jsonify, request

class LogAsunto:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def get_logs(self):
        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            logs = self.models.LOG_ASUNTO.query.order_by(self.models.LOG_ASUNTO.expediente).paginate(
                page=page, per_page=per_page, error_out=False)

            if not logs.items:
                return jsonify({'message': 'No hay registros de log'}), 404

            return jsonify({
                'logs': [log.to_dict() for log in logs.items],
                'total': logs.total,
                'pagina_actual': logs.page,
                'total_paginas': logs.pages
            }), 200

        except Exception as e:
            print("Error en get_logs:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def get_log_by_id(self, id):
        try:
            log = self.models.LOG_ASUNTO.query.filter_by(id=id).first()

            if not log:
                return jsonify({'message': 'Registro de log no encontrado'}), 404

            return jsonify(log.to_dict()), 200

        except Exception as e:
            print("Error en get_log_by_id:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def create_log(self, json_data):
        try:
            expediente = json_data.get('expediente')
            accion = json_data.get('accion')

            if not expediente or not accion:
                return jsonify({'message': "'expediente' y 'accion' son requeridos"}), 400

            nuevo_log = self.models.LOG_ASUNTO(
                expediente=expediente,
                accion=accion
            )
            self.db.session.add(nuevo_log)
            self.db.session.commit()

            return jsonify({
                'message': 'Registro de log creado',
                'log': nuevo_log.to_dict()
            }), 201

        except Exception as e:
            print("Error en create_log:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500

    def update_log(self, id, json_data):
        try:
            log = self.models.LOG_ASUNTO.query.filter_by(id=id).first()

            if not log:
                return jsonify({'message': 'Registro de log no encontrado'}), 404

            accion = json_data.get('accion')

            if accion:
                log.accion = accion

            self.db.session.commit()

            return jsonify({
                'message': 'Registro de log actualizado',
                'log': log.to_dict()
            }), 200

        except Exception as e:
            print("Error en update_log:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500
    def innerJoin(self):
        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            logs = self.models.LOG_ASUNTO.query.order_by(self.models.LOG_ASUNTO.expediente).paginate(
                page=page, per_page=per_page, error_out=False)

            if not logs.items:
                return jsonify({'message': 'No hay registros de log'}), 404

            enriched_logs = []
            for log in logs.items:
                expediente = log.expediente

                asunto_sv = self.models.ASUNTO_SV.query.filter_by(expediente=expediente).first()
                asunto_mx = self.models.ASUNTO_MX.query.filter_by(expediente=expediente).first() if not asunto_sv else None

                asunto = asunto_sv or asunto_mx

                enriched_logs.append({
                    'log': log.to_dict(),
                    'asunto': asunto.to_dict() if asunto else None
                })

            return jsonify({
                'logs': enriched_logs,
                'total': logs.total,
                'pagina_actual': logs.page,
                'total_paginas': logs.pages
            }), 200

        except Exception as e:
            print("Error en get_logs:", e)
            return jsonify({'message': 'Error interno del servidor'}), 500
