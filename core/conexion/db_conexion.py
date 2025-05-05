import os
from dotenv import load_dotenv

if not load_dotenv(override=True):
    print("Warning: .env file not found or could not be loaded.")

class ConexionDB:
    def __init__(self):
        # México (MySQL)
        self.user_mysql_mx = os.getenv("DB_USER_MYSQL_MX")
        self.pass_mysql_mx = os.getenv("DB_PASSWORD_MYSQL_MX")
        self.db_mysql_mx = os.getenv("DB_NAME_MYSQL_MX")
        self.host_mysql_mx = os.getenv("DB_HOST_MYSQL_MX")
        self.port_mysql_mx = os.getenv("DB_PORT_MYSQL_MX")

        # El Salvador (MySQL)
        self.user_mysql_sv = os.getenv("DB_USER_MYSQL_SV")
        self.pass_mysql_sv = os.getenv("DB_PASSWORD_MYSQL_SV")
        self.db_mysql_sv = os.getenv("DB_NAME_MYSQL_SV")
        self.host_mysql_sv = os.getenv("DB_HOST_MYSQL_SV")
        self.port_mysql_sv = os.getenv("DB_PORT_MYSQL_SV")

        # Oracle (sede central)
        self.host_oracle = os.getenv("DB_HOST_ORACLE")
        self.user_oracle = os.getenv("DB_USER_ORACLE")
        self.password_oracle = os.getenv("DB_PASSWORD_ORACLE")
        self.database_oracle = os.getenv("DB_NAME_ORACLE")
        self.port_oracle = os.getenv("DB_PORT_ORACLE")

    def connect_mysql_mexico(self):
        return (
            f"mysql+mysqlconnector://{self.user_mysql_mx}:{self.pass_mysql_mx}"
            f"@{self.host_mysql_mx}:{self.port_mysql_mx}/{self.db_mysql_mx}"
        )

    def connect_mysql_elsalvador(self):
        return (
            f"mysql+mysqlconnector://{self.user_mysql_sv}:{self.pass_mysql_sv}"
            f"@{self.host_mysql_sv}:{self.port_mysql_sv}/{self.db_mysql_sv}"
        )

    def connect_oracle(self):
        return (
            f"oracle+oracledb://{self.user_oracle}:{self.password_oracle}@"
            f"{self.host_oracle}:{self.port_oracle}/?service_name={self.database_oracle}"
        )
