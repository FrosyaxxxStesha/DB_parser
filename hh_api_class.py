from requests import get
from accessify import private, protected
from json import loads, dumps
from datetime import datetime


class HeadHunterAPI:
    __base_url: str = 'https://api.hh.ru/'
    __emp_url: str = __base_url + 'employers/'
    __vac_url: str = __base_url + 'vacancies'

    def __init__(self, emp_id_list):
        self.__emp_id_list = emp_id_list

    def connect_api_emp(self, emp_id):
        with get(self.__emp_url + emp_id) as response:
            emp_dict = response.json()
        return emp_dict

    def get_employers(self) -> list:
        return [self.connect_api_emp(emp_id) for emp_id in self.__emp_id_list]

    def connect_api_vacs(self, emp_id, per_page=100):
        params = dict(employer_id=emp_id, per_page=per_page)
        with get(self.__vac_url, params=params) as response:
            vacs = response.json()
        return vacs['items']

    def get_vacs(self):
        vac_list = []

        for emp_id in self.__emp_id_list:
            vac_list.extend(self.connect_api_vacs(emp_id))

        return vac_list

    @staticmethod
    def normalize_emp(emp_dict):
        normalized_tuple = (
            int(emp_dict["id"]),
            emp_dict["trusted"],
            emp_dict["name"],
            emp_dict["type"],
            emp_dict["area"]["name"],
            emp_dict["open_vacancies"],
            emp_dict["site_url"],
            emp_dict["alternate_url"],
            emp_dict["vacancies_url"],
            emp_dict["description"]
        )

        return normalized_tuple

    @staticmethod
    def normalize_vac(vac_dict):
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
            vac_dict["address"],
            vac_dict["url"],
            vac_dict["snippet"]["requirement"],
            vac_dict["snippet"]["responsibility"]
        )

        return normalized_tuple


f = HeadHunterAPI([str(9498112)])
print(dumps(f.get_vacs(), ensure_ascii=False, indent=2))
