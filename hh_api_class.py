from requests import get
from accessify import private


class HeadHunterAPI:
    __base_url: str = 'https://api.hh.ru/'
    __emp_url: str = __base_url + 'employers/'
    __vac_url: str = __base_url + 'vacancies'

    def __init__(self):
        self.emp_list = []

    @private
    def connect_api_emp(self, emp_id):
        with get(self.__emp_url + emp_id) as response:
            emp_dict = response.json()
        return emp_dict

    def get_employers(self, emp_id_list: list) -> list:
        return [self.connect_api_emp(emp_id) for emp_id in emp_id_list]

    def connect_api_vacs(self, emp_id, per_page=100):
        params = dict(employer_id=emp_id, per_page=per_page)
        with get(self.__vac_url, params=params) as response:
            vacs = response.json()
        return vacs['items']

    def get_vacs(self, emp_id_list):
        vac_list = []

        for emp_id in emp_id_list:
            vac_list.extend(self.connect_api_vacs(emp_id))

        return vac_list

    def normalize_emp(self):
        pass

    def normalize_vac(self):
        pass
