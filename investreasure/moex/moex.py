from settings import (
    MAIN_URL,
    AUTH_URL,
    REQUEST_RETURN_TYPE,
)
from local_settings import (
    MOEX_LOGIN,
    MOEX_PASSWORD,
)

from common.api import regular_request
import requests
from requests.auth import HTTPBasicAuth


class Moex:

    moex_site = MAIN_URL
    moex_auth_site = AUTH_URL
    request_return_type = REQUEST_RETURN_TYPE
    road_map = {
        'base': {
            'index': '/index.'
        },
        'history': {
            'shares': '/history/engines/stock/markets/shares/securities.',
            'bonds': '/history/engines/stock/markets/bonds/securities.'
        }
    }
    login = MOEX_LOGIN
    password = MOEX_PASSWORD
    token = None

    def __init__(self):
        self.cookies = self.auth()

    @staticmethod
    def for_normal_dict(raw_dict: dict) -> dict:
        normal_dict = {}
        for key, val in raw_dict.items():
            if key == 'metadata':
                continue
            normal_dict[key] = []
            for data in val['data']:
                row = dict(zip(val['columns'], data))
                normal_dict[key].append(row)
        return normal_dict

    def moex_request(self, road_map_path: str, params=None) -> dict:
        url = f'{self.moex_site}{road_map_path}{self.request_return_type}'
        url += f'{params}' if params else ''
        data = regular_request(
            url=f'{url}{road_map_path}{self.request_return_type}',
            cookies=self.cookies
        )
        return self.for_normal_dict(data)

    def auth(self):
        auth = HTTPBasicAuth(self.login, self.password)
        data = requests.get(
            url=f'{self.moex_auth_site}',
            auth=auth)
        return dict(data.cookies)


moex = Moex()
