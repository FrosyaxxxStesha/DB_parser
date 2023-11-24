from hh_api_class import HeadHunterAPI
from sql_executor_class import SQLExecutor


with open("employers_ids.txt") as fp:
    data = fp.read()
emp_list = data.split("\n")

hh_api = HeadHunterAPI(emp_list)
vacs = hh_api.get_vacs()
employers = hh_api.get_employers()

with SQLExecutor(config_file="database.ini") as executor:
    executor.create_tables()
    executor.fill_table(employers, "employers")
    executor.fill_table(vacs, "vacancies")
