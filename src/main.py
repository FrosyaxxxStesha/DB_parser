from src.classes.hh_api_class import HeadHunterAPI
from src.classes.sql_executor_class import SQLExecutor

# Получение списка id работодателей
with open("determ_files/employers_ids.txt") as fp:
    data = fp.read()
emp_list = data.split("\n")

# Получение данных от API
hh_api = HeadHunterAPI(emp_list)
vacs = hh_api.get_vacs()
employers = hh_api.get_employers()


# Заполнение таблицы данными
with SQLExecutor(config_file="database.ini") as executor:
    executor.create_tables()
    executor.fill_table(employers, "employers")
    executor.fill_table(vacs, "vacancies")
