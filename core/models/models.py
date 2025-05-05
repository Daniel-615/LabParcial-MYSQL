class Models:
    def __init__(self, db):
        self.db = db

        # --- MYSQL - El Salvador ---
        class CLIENTE_SV(db.Model):
            __tablename__ = 'CLIENTE'
            __bind_key__ = 'salvador'
            id = db.Column(db.Integer, primary_key=True)
            nombre = db.Column(db.String(255), nullable=False)
            direccion = db.Column(db.String(255))
            telefono = db.Column(db.String(50))
            email = db.Column(db.String(100))

            def to_dict(self):
                return {
                    'id': self.id,
                    'nombre': self.nombre,
                    'direccion': self.direccion,
                    'telefono': self.telefono,
                    'email': self.email
                }

        self.CLIENTE_SV = CLIENTE_SV

        class ASUNTO_SV(db.Model):
            __tablename__ = 'ASUNTO'
            __bind_key__ = 'salvador'
            expediente = db.Column(db.String(100), primary_key=True)
            fecha_inicio = db.Column(db.Date, default=db.func.current_date())
            fecha_fin = db.Column(db.Date)
            estado = db.Column(db.String(50))
            cliente_id = db.Column(db.Integer, db.ForeignKey('CLIENTE.id'), nullable=False)

            def to_dict(self):
                return{
                    'expediente': self.expediente,
                    'fecha_inicio': self.fecha_inicio,
                    'fecha_fin': self.fecha_fin,
                    'estado': self.estado,
                    'cliente_id': self.cliente_id
                }

        self.ASUNTO_SV = ASUNTO_SV

        class ABOGADO_SV(db.Model):
            __tablename__ = 'ABOGADO'
            __bind_key__ = 'salvador'
            dni = db.Column(db.String(50), primary_key=True)
            nombre = db.Column(db.String(255), nullable=False)
            gabinete_id = db.Column(db.Integer, db.ForeignKey('GABINETE.id'), nullable=False)
            def to_dict(self):
                return{
                    'dni': self.dni,
                    'nombre': self.nombre,
                    'gabinete_id': self.gabinete_id
                }

        self.ABOGADO_SV = ABOGADO_SV

        class GABINETE_SV(db.Model):
            __tablename__ = 'GABINETE'
            __bind_key__ = 'salvador'
            id = db.Column(db.Integer, primary_key=True)
            nombre = db.Column(db.String(255), nullable=False)
            pais = db.Column(db.String(100))
            sistema_operativo = db.Column(db.String(100))

            def to_dict(self):
                return{
                    'id': self.id,
                    'nombre': self.nombre,
                    'pais': self.pais,
                    'sistema_operativo': self.sistema_operativo
                }

        self.GABINETE_SV = GABINETE_SV


        class AUDIENCIA_SV(db.Model):
            __tablename__ = 'AUDIENCIA'
            __bind_key__ = 'salvador'
            id = db.Column(db.Integer, primary_key=True)
            asunto_exp = db.Column(db.String(100), db.ForeignKey('ASUNTO.expediente'), nullable=False)
            fecha = db.Column(db.DateTime, nullable=False)
            abogado_dni= db.Column(db.String(50), db.ForeignKey('ABOGADO.dni'), nullable=False)

            def to_dict(self):
                return{
                    'id': self.id,
                    'asunto_exp': self.asunto_exp,
                    'fecha': self.fecha,
                    'abogado_dni': self.abogado_dni
                }
        self.AUDIENCIA_SV = AUDIENCIA_SV

        class INCIDENCIA_SV(db.Model):
            __tablename__ = 'INCIDENCIA'
            __bind_key__ = 'salvador'
            id = db.Column(db.Integer, primary_key=True)
            audiencia_id = db.Column(db.Integer, db.ForeignKey('AUDIENCIA.id'), nullable=False)
            descripcion = db.Column(db.String(1000), nullable=False)

            def to_dict(self):
                return{
                    'id': self.id,
                    'audiencia_id': self.audiencia_id,
                    'descripcion': self.descripcion
                }

        self.INCIDENCIA_SV = INCIDENCIA_SV

        # --- MYSQL - Mexico ---
        class CLIENTE_MX(db.Model):
            __tablename__ = 'CLIENTE'
            __bind_key__ = 'mexico'
            id = db.Column(db.Integer, primary_key=True)
            nombre = db.Column(db.String(255), nullable=False)
            direccion = db.Column(db.String(255))
            telefono = db.Column(db.String(50))
            email = db.Column(db.String(100))

            def to_dict(self):
                return {
                    'id': self.id,
                    'nombre': self.nombre,
                    'direccion': self.direccion,
                    'telefono': self.telefono,
                    'email': self.email
                }

        self.CLIENTE_MX = CLIENTE_MX

        class ASUNTO_MX(db.Model):
            __tablename__ = 'ASUNTO'
            __bind_key__ = 'mexico'
            expediente = db.Column(db.String(100), primary_key=True)
            fecha_inicio = db.Column(db.Date, default=db.func.current_date())
            fecha_fin = db.Column(db.Date)
            estado = db.Column(db.String(50))
            cliente_id = db.Column(db.Integer, db.ForeignKey('CLIENTE.id'), nullable=False)

            def to_dict(self):
                return{
                    'expediente': self.expediente,
                    'fecha_inicio': self.fecha_inicio,
                    'fecha_fin': self.fecha_fin,
                    'estado': self.estado,
                    'cliente_id': self.cliente_id
                }

        self.ASUNTO_MX = ASUNTO_MX

        class ABOGADO_MX(db.Model):
            __tablename__ = 'ABOGADO'
            __bind_key__ = 'mexico'
            dni = db.Column(db.String(50), primary_key=True)
            nombre = db.Column(db.String(255), nullable=False)
            gabinete_id = db.Column(db.Integer, db.ForeignKey('GABINETE.id'), nullable=False)

            def to_dict(self):
                return{
                    'dni': self.dni,
                    'nombre': self.nombre,
                    'gabinete_id': self.gabinete_id
                }

        self.ABOGADO_MX = ABOGADO_MX

        class GABINETE_MX(db.Model):
            __tablename__ = 'GABINETE'
            __bind_key__ = 'mexico'
            id = db.Column(db.Integer, primary_key=True)
            nombre = db.Column(db.String(255), nullable=False)
            pais = db.Column(db.String(100))
            sistema_operativo = db.Column(db.String(100))
            def to_dict(self):
                return{
                    'id': self.id,
                    'nombre': self.nombre,
                    'pais': self.pais,
                    'sistema_operativo': self.sistema_operativo
                }

        self.GABINETE_MX = GABINETE_MX


        class AUDIENCIA_MX(db.Model):
            __tablename__ = 'AUDIENCIA'
            __bind_key__ = 'mexico'
            id = db.Column(db.Integer, primary_key=True)
            asunto_exp = db.Column(db.String(100), db.ForeignKey('ASUNTO.expediente'), nullable=False)
            fecha = db.Column(db.DateTime, nullable=False)
            abogado_dni = db.Column(db.String(50), db.ForeignKey('ABOGADO.dni'), nullable=False)

            def to_dict(self):
                return {
                    'id': self.id,
                    'asunto_exp': self.asunto_exp,
                    'fecha': self.fecha,
                    'abogado_dni': self.abogado_dni
                }

        self.AUDIENCIA_MX = AUDIENCIA_MX

        class INCIDENCIA_MX(db.Model):
            __tablename__ = 'INCIDENCIA'
            __bind_key__ = 'mexico'
            id = db.Column(db.Integer, primary_key=True)
            audiencia_id = db.Column(db.Integer, db.ForeignKey('AUDIENCIA.id'), nullable=False)
            descripcion = db.Column(db.String(1000), nullable=False)

            def to_dict(self):
                return{
                    'id': self.id,
                    'audiencia_id': self.audiencia_id,
                    'descripcion': self.descripcion
                }

        self.INCIDENCIA_MX = INCIDENCIA_MX

        # --- Oracle - Central ---
        class LOG_ASUNTO(db.Model):
            __bind_key__ = 'oracle'
            __tablename__ = 'LOG_ASUNTO'
            id = db.Column(db.Integer, primary_key=True)
            expediente = db.Column(db.String(100), nullable=False)
            accion = db.Column(db.String(50), nullable=False)
            timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

            def to_dict(self):
                return{
                    'id': self.id,
                    'expediente': self.expediente,
                    'accion': self.accion,
                    'timestamp': self.timestamp
                }

        self.LOG_ASUNTO = LOG_ASUNTO
    # Diccionarios para acceder por sede
        self.ASUNTO = {
            'salvador': self.ASUNTO_SV,
            'mexico': self.ASUNTO_MX
        }

        self.CLIENTE = {
            'salvador': self.CLIENTE_SV,
            'mexico': self.CLIENTE_MX
        }

        self.ABOGADO = {
            'salvador': self.ABOGADO_SV,
            'mexico': self.ABOGADO_MX
        }

        self.GABINETE = {
            'salvador': self.GABINETE_SV,
            'mexico': self.GABINETE_MX
        }

        self.AUDIENCIA = {
            'salvador': self.AUDIENCIA_SV,
            'mexico': self.AUDIENCIA_MX
        }

        self.INCIDENCIA = {
            'salvador': self.INCIDENCIA_SV,
            'mexico': self.INCIDENCIA_MX
        }
