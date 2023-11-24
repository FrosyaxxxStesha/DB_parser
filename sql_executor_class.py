import psycopg2
from config import config
from json import dumps


class SQLExecutor:
    def __init__(self,
                 password=None,
                 host="localhost",
                 user="postgres",
                 database="headhunter",
                 port="5432",
                 config_file=None
                 ):
        init_by_config = True

        if config_file is None:
            init_by_config = False
            if password is None:
                raise ValueError("пароль не введён")

        if init_by_config:
            params = config()
        else:
            params = dict(
                host=host,
                user=user,
                database=database,
                port=port,
                password=password
                          )

        self.__params = params
        self.__conn = None

    def connect(self):
        if self.__conn is None:
            self.__conn = psycopg2.connect(**self.__params)
        return self.__conn

    def close(self):
        if self.__conn is not None:
            self.__conn.commit()
            self.__conn.close()
            self.__conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def get_script(script: str):
        if script.endswith(".sql"):
            with open(script) as fp:
                script = fp.read()
        return script

    def execute(self, sql_script):
        print(sql_script)
        with self.__conn.cursor() as cur:
            cur.execute(sql_script)

    def create_tables(self, script="sql_scripts/create_db.sql"):
        sql_script = self.get_script(script)
        self.execute(sql_script)

    def fill_table(self, items: list[tuple], table_name: str, script: str = "sql_scripts/fill_template.sql") -> None:
        prepared_list = [str(i).replace("''", "NULL").replace("None", "NULL")
                         for i in items]

        value_string = ",\n".join(prepared_list)
        sql_script_template = self.get_script(script)

        sql_script = sql_script_template.replace("{name_place}", table_name)
        sql_script = sql_script.replace("{values_place}", value_string)

        self.execute(sql_script)
