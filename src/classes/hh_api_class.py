from requests import get
from datetime import datetime


class HeadHunterAPI:
    """Класс для работы с API hh.ru"""
    __base_url: str = 'https://api.hh.ru/'
    __emp_url: str = __base_url + 'employers/'
    __vac_url: str = __base_url + 'vacancies'

    def __init__(self, emp_id_list: list[str]) -> None:
        self.__emp_id_list = emp_id_list

    def connect_api_emp(self, emp_id: str) -> dict:
        """Метод для получения данных об одном работодателе"""
        with get(self.__emp_url + emp_id) as response:
            emp_dict = response.json()
        return emp_dict

    def get_employers(self) -> list:
        """Метод для получения готовых данных о списке работодателей"""
        return [self.normalize_emp(self.connect_api_emp(emp_id)) for emp_id in self.__emp_id_list]

    def connect_api_vac(self, emp_id: str, per_page: int = 100) -> list[dict]:
        """Метод для получения данных о вакансиях одного работодателя"""
        params = dict(employer_id=emp_id, per_page=per_page)
        with get(self.__vac_url, params=params) as response:
            vacs = response.json()
        return vacs['items']

    def get_vacs(self) -> list:
        """Метод для получения готовых данных о вакансиях по списку работодателей"""
        vac_list = []

        for emp_id in self.__emp_id_list:
            vac_list.extend(self.normalize_vac(i) for i in self.connect_api_vac(emp_id))

        return vac_list

    @staticmethod
    def normalize_emp(emp_dict: dict) -> tuple:
        """Метод для приведения данных о работодателе в удобный для БД вид"""
        normalized_tuple = (
            int(emp_dict["id"]),
            emp_dict["trusted"],
            emp_dict["name"],
            emp_dict["type"],
            emp_dict["area"]["name"],
            emp_dict["site_url"],
            emp_dict["alternate_url"],
            emp_dict["vacancies_url"],
            emp_dict["description"]
        )

        return normalized_tuple

    @staticmethod
    def normalize_vac(vac_dict: dict) -> tuple:
        """Метод для приведения данных о вакансии в удобный для БД вид"""
        if vac_dict["salary"] is None:
            salary = None
        elif vac_dict["salary"]["from"] is None and vac_dict["salary"]["to"] is None:
            salary = None
        elif vac_dict["salary"]["from"] is None:
            salary = vac_dict["salary"]["to"]
        elif vac_dict["salary"]["to"] is None:
            salary = vac_dict["salary"]["from"]
        else:
            salary = (vac_dict["salary"]["from"] + vac_dict["salary"]["to"]) / 2

        if (publ := vac_dict["published_at"]) is not None:
            dt = str(datetime.fromisoformat(publ))
        else:
            dt = None

        normalized_tuple = (
            int(vac_dict["id"]),
            int(vac_dict["employer"]["id"]),
            dt,
            vac_dict["name"],
            vac_dict["area"]["name"],
            salary,
            vac_dict["url"]
        )

        return normalized_tuple
