import psycopg2
from config import config


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
        elif password is None:
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
            self.__conn = psycopg2.connect()
        return self.__conn

    def close(self):
        if self.__conn is not None:
            self.__conn.close()
            self.__conn = None

    def __enter__(self):
        return self.connect()

    def __exit__(self):
        self.close()

    @staticmethod
    def get_script(script: str):
        if script.endswith(".sql"):
            with open(script) as fp:
                script = fp.read()
        return script

    def execute(self, sql_script):
        with self.__conn.cursor() as cur:
            cur.execute(sql_script)

    def create_tables(self, script="sql_scripts/create_db.sql"):
        sql_script = self.get_script(script)
        self.execute(sql_script)

    def fill_table(self, items: list[tuple], script_template: str) -> None:
        prepared_list = [str(i) for i in items]
        emp_string = ",\n".join(prepared_list)
        sql_script_template = self.get_script(script_template)

        sql_script = sql_script_template.replace("{placeholder}", emp_string)
        self.execute(sql_script)
