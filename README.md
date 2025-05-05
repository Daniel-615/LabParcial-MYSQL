
Configuración del Proyecto

Este proyecto se conecta a múltiples bases de datos distribuidas en distintos países. A continuación, se detallan las variables de entorno necesarias y las instrucciones para ejecutar el entorno de desarrollo.

Bases de Datos

MySQL - México

DB_HOST_MYSQL_MX=192.168.1.147  
DB_USER_MYSQL_MX=root  
DB_PASSWORD_MYSQL_MX=angel1234!  
DB_NAME_MYSQL_MX=lab_mexico  
DB_PORT_MYSQL_MX=3310

MySQL - El Salvador

DB_HOST_MYSQL_SV=192.168.1.148  
DB_USER_MYSQL_SV=root  
DB_PASSWORD_MYSQL_SV=angel1234!  
DB_NAME_MYSQL_SV=lab_salvador  
DB_PORT_MYSQL_SV=3310

Oracle - Guatemala (Sede Central)

DB_USER_ORACLE=SYSTEM  
DB_PASSWORD_ORACLE=1234  
DB_NAME_ORACLE=xepdb1  
DB_HOST_ORACLE=localhost  
DB_PORT_ORACLE=1522

Instrucciones

1. Crear entorno virtual y descargar dependencias

Ejecuta el siguiente script en tu terminal (Windows):

./setup.bat

2. Levantar el proyecto

Una vez configurado el entorno, ejecuta:

flask run
