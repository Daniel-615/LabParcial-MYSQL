# CONTROLADORES
from core.labA.controladores.cliente_controlador import Cliente as ClienteController
from core.labA.controladores.asunto_controlador import Asunto as AsuntoController
from core.labA.controladores.abogado_controlador import Abogado as AbogadoController
from core.labA.controladores.gabinete_controlador import Gabinete as GabineteController
from core.labA.controladores.audiencia_controlador import Audiencia as AudienciaController
from core.labA.controladores.incidencia_controlador import Incidencia as IncidenciaController
from core.labA.controladores.log_asunto_controlador import LogAsunto as LogAsuntoController

# RUTAS
from core.labA.rutas.cliente_ruta import Cliente as ClienteRoute
from core.labA.rutas.asunto_ruta import Asunto as AsuntoRoute
from core.labA.rutas.abogado_ruta import Abogado as AbogadoRoute
from core.labA.rutas.gabinete_ruta import Gabinete as GabineteRoute
from core.labA.rutas.audiencia_ruta import Audiencia as AudienciaRoute
from core.labA.rutas.incidencia_ruta import Incidencia as IncidenciaRoute
from core.labA.rutas.log_asunto_ruta import LogAsunto as LogAsuntoRoute

class Configuracion:
    def __init__(self, app, db, models):
        self.app = app
        self.db = db
        self.models = models

        # Controladores SQL Server por sede
        self.controllers_mysql('salvador')
        self.controllers_mysql('mexico')
        self.controllers_oracle()

        # Rutas
        self.routes_mysql('salvador')
        self.routes_mysql('mexico')
        self.routes_oracle()

    # MYSQL: Getters generales por sede
    def getClienteController(self, sede): return self.cliente[sede]
    def getAsuntoController(self, sede): return self.asunto[sede]
    def getAbogadoController(self, sede): return self.abogado[sede]
    def getGabineteController(self, sede): return self.gabinete[sede]
    def getAbogadoGabineteController(self, sede): return self.abogado_gabinete[sede]
    def getAudienciaController(self, sede): return self.audiencia[sede]
    def getIncidenciaController(self, sede): return self.incidencia[sede]

    # Oracle: Getter único
    def getLogAsuntoController(self): return self.log_asunto

    def controllers_mysql(self, sede):
        if not hasattr(self, 'cliente'):
            self.cliente = {}
            self.asunto = {}
            self.abogado = {}
            self.gabinete = {}
            self.abogado_gabinete = {}
            self.audiencia = {}
            self.incidencia = {}

        self.cliente[sede] = ClienteController(self.db, self.models, sede)
        self.asunto[sede] = AsuntoController(self.db, self.models, sede)
        self.abogado[sede] = AbogadoController(self.db, self.models, sede)
        self.gabinete[sede] = GabineteController(self.db, self.models, sede)
        self.audiencia[sede] = AudienciaController(self.db, self.models, sede)
        self.incidencia[sede] = IncidenciaController(self.db, self.models, sede)

    def controllers_oracle(self):
        self.log_asunto = LogAsuntoController(self.db, self.models)

    def routes_mysql(self, sede):
        ClienteRoute(self.app, self, sede)
        AsuntoRoute(self.app, self, sede)
        AbogadoRoute(self.app, self, sede)
        GabineteRoute(self.app, self, sede)
        AudienciaRoute(self.app, self, sede)
        IncidenciaRoute(self.app, self, sede)

    def routes_oracle(self):
        LogAsuntoRoute(self.app, self)