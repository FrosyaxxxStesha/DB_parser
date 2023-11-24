from src.classes.sql_executor_class import SQLExecutor


class DBManager(SQLExecutor):
    """Класс для выборки данных из БД"""
    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Получить Список компаний и количество вакансий у каждой"""
        script = self.get_script("sql_scripts/get_companies_and_vacs_count.sql")
        return self.execute_select(script)

    def get_all_vacancies(self) -> list[tuple]:
        """Получить все вакансии"""
        script = self.get_script("sql_scripts/get_all_vacancies.sql")
        return self.execute_select(script)

    def get_avg_salary(self) -> list[tuple]:
        """Получить среднюю зарплату по всем вакансиям"""
        script = self.get_script("sql_scripts/get_avg_salary.sql")
        return self.execute_select(script)

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Получить вакансии с зарплатой выше средней"""
        script = self.get_script("sql_scripts/get_higher_salary_vacs.sql")
        return self.execute_select(script)

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Получить вакансию по ключевому слову в названии"""
        script = self.get_script("sql_scripts/get_vacancies_with_kw.sql")
        script = script.replace("{keyword}", keyword)
        return self.execute_select(script)
