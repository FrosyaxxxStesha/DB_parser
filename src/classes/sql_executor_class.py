import psycopg2
from src.config import config


class SQLExecutor:
    """Класс для выполнения SQL-запросов"""
    def __init__(self,
                 password=None,
                 host="localhost",
                 user="postgres",
                 database="headhunter",
                 port="5432",
                 config_file=None
                 ) -> None:
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
        """Метод для подключения к БД"""
        if self.__conn is None:
            self.__conn = psycopg2.connect(**self.__params)
        return self.__conn

    def close(self) -> None:
        """Метод для разрыва соединения с БД"""
        if self.__conn is not None:
            self.__conn.commit()
            self.__conn.close()
            self.__conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    @staticmethod
    def get_script(script: str) -> str:
        """Метод для получения скрипта из файла"""
        if script.endswith(".sql"):
            with open(script) as fp:
                script = fp.read()
        return script

    def execute(self, sql_script: str) -> None:
        """Метод для выполнения запросов без возврата данных"""
        with self.__conn.cursor() as cur:
            cur.execute(sql_script)

    def execute_select(self, sql_script: str) -> list[tuple]:
        """Метод для выполнения запроса с возвратом данных"""
        with self.__conn.cursor() as cur:
            cur.execute(sql_script)
            data = cur.fetchall()
        return data

    def create_tables(self, script: str = "sql_scripts/create_db.sql") -> None:
        """Метод для создания таблиц"""
        sql_script = self.get_script(script)
        self.execute(sql_script)

    def fill_table(self, items: list[tuple], table_name: str, script: str = "sql_scripts/fill_template.sql") -> None:
        """Метод для заполнения таблиц"""
        prepared_list = [str(i).replace("''", "NULL").replace("None", "NULL")
                         for i in items]

        value_string = ",\n".join(prepared_list)
        sql_script_template = self.get_script(script)

        sql_script = sql_script_template.replace("{name_place}", table_name)
        sql_script = sql_script.replace("{values_place}", value_string)

        self.execute(sql_script)
