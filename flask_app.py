from flask import Flask
from core.conexion.db_conexion import ConexionDB
from core.models.models import Models
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from core.labA.TriggersOracle import TriggersOracle
from core.configuracion.configuracion import Configuracion
import time
import socket
import os
class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.conexion = ConexionDB()

        try:
            wait_for_db("mysql_mexico", 3306)
            wait_for_db("mysql_salvador", 3306)
            wait_for_db("oracle_guatemala", 1521)
            uri_mexico = self.conexion.connect_mysql_mexico()
            uri_elsalvador = self.conexion.connect_mysql_elsalvador()
            uri_oracle = self.conexion.connect_oracle()

            if not all([ uri_mexico, uri_elsalvador, uri_oracle]):
                raise ValueError("Faltan una o más URIs de conexión a las bases de datos.")

            self.app.config['SQLALCHEMY_DATABASE_URI'] = uri_oracle

            self.app.config['SQLALCHEMY_BINDS'] = {
                'mexico': uri_mexico,
                'salvador': uri_elsalvador,
                'oracle': uri_oracle #guatemala
            }

        except Exception as e:
            print(f"\n Error al establecer conexiones a las bases de datos: {e}\n")

        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db = SQLAlchemy(self.getApp())
        self.models = Models(self.db)

        self.app_initializer = Configuracion(self.getApp(), self.db, self.models)

        with self.app.app_context():
            self.db.create_all()
            oracle_helper = TriggersOracle(self.db)
            oracle_helper.create_auto_increment("LOG_ASUNTO")

        self.migrate = Migrate(self.getApp(), self.db)

    def startApp(self):
        self.app.run(debug=True, host="0.0.0.0", port=5000)

    def getApp(self):
        return self.app


def wait_for_db(host, port, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            socket.create_connection((host, port))
            return True
        except OSError:
            time.sleep(1)
    raise RuntimeError(f"No se pudo conectar a {host}:{port} en {timeout} segundos")
