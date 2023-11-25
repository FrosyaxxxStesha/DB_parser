from src.classes.db_manager_class import DBManager


def pretty_view(lst) -> None:
    for i in lst:
        print(i)


def interact():
    with DBManager(config_file="database.ini") as db_manager:
        action = ""
        action_func_dict = {
            "get vacs --count": db_manager.get_companies_and_vacancies_count,
            "get vacs": db_manager.get_all_vacancies,
            "get avg salary": db_manager.get_avg_salary,
            "get vacs --high salary": db_manager.get_vacancies_with_higher_salary
        }

        while action != "exit":
            action = input("database_viewer>>> ")
            if action not in action_func_dict and not action.startswith("get vacs --keyword ") and action != "exit":
                print("такой команды не существует")
                continue

            elif action in action_func_dict:
                pretty_view(action_func_dict[action]())
                continue

            elif action.startswith("get vacs --keyword "):
                keyword = action.split(" ", maxsplit=3)[-1]
                pretty_view(db_manager.get_vacancies_with_keyword(keyword))
                continue


interact()




