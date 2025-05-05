class TriggersOracle:

    def __init__(self, db):
        self.engine = db.get_engine(bind='oracle')

    def create_auto_increment(self, table_name, pk_column='id'):
        sequence_name = f"SEQ_{table_name.upper()}"
        trigger_name = f"TRG_{table_name.upper()}_BI"

        create_sequence_sql = f"""
        BEGIN
            EXECUTE IMMEDIATE '
                CREATE SEQUENCE {sequence_name}
                START WITH 1
                INCREMENT BY 1
                NOCACHE
            ';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN
                    RAISE;
                END IF;
        END;
        """

        create_trigger_sql = f"""
        CREATE OR REPLACE TRIGGER {trigger_name}
        BEFORE INSERT ON {table_name}
        FOR EACH ROW
        WHEN (NEW.{pk_column} IS NULL)
        BEGIN
            SELECT {sequence_name}.NEXTVAL INTO :NEW.{pk_column} FROM dual;
        END;
        """

        with self.engine.connect() as conn:
            try:
                # Usa el cursor crudo para evitar el error de SQLAlchemy con :NEW
                raw_conn = conn.connection
                cursor = raw_conn.cursor()
                cursor.execute(create_sequence_sql)
                cursor.execute(create_trigger_sql)
                print(f"Secuencia y trigger creados para {table_name}")
            except Exception as e:
                print(f"Error al crear secuencia/trigger para {table_name}: {e}")
