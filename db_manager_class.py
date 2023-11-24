from sql_executor_class import SQLExecutor


class DBManager(SQLExecutor):
    def execute_select(self, sql_script):
        with self.__conn.cursor() as cur:
            cur.execute(sql_script)
            data = cur.fetchall()
        return data

    def get_companies_and_vacancies_count(self):
        script = self.get_script("sql_scripts/get_companies_and_vacs_count.sql")
        return self.execute_select(script)

    def get_all_vacancies(self):
        script = self.get_script("sql_scripts/get_all_vacancies.sql")
        return self.execute_select(script)

    def get_avg_salary(self):
        script = self.get_script("sql_scripts/get_avg_salary.sql")
        return self.execute_select(script)

    def get_vacancies_with_higher_salary(self):
        script = self.get_script("sql_scripts/get_higher_salary_vacs.sql")
        return self.execute_select(script)

    def get_vacancies_with_keyword(self, keyword):
        script = self.get_script("sql_scripts/get_all_vacancies.sql")
        script = script.replace("{placeholder}", keyword)
        return self.execute_select(script)
