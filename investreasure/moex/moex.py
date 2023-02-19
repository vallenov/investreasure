import json
import logging
import requests
from requests.auth import HTTPBasicAuth
from requests.models import Response

from settings import (
    MAIN_URL,
    AUTH_URL,
    REQUEST_RETURN_TYPE,
)
from local_settings import (
    MOEX_LOGIN,
    MOEX_PASSWORD,
)

from common.api import (
    regular_request,
    BaseResponse,
    BaseMetadata,
)

logger = logging.getLogger('index')


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
            'bonds': '/history/engines/stock/markets/bonds/securities.',
            'index': '/history/engines/stock/markets/index/securities.'
        }
    }
    login = MOEX_LOGIN
    password = MOEX_PASSWORD

    def __init__(self):
        self.cookies = self.auth()

    @staticmethod
    def for_normal_dict(text: str) -> dict:
        normal_dict = {}
        raw_dict: dict = json.loads(text)
        for key, val in raw_dict.items():
            if key == 'metadata':
                continue
            low_vals = [low.lower() for low in val['columns']]
            normal_dict[key] = []
            for data in val['data']:
                row = dict(zip(low_vals, data))
                normal_dict[key].append(row)
        return normal_dict

    def moex_request(self, road_map_path: str, params=None) -> BaseResponse:
        url = f'{self.moex_site}{road_map_path}{self.request_return_type}'
        url += f'{params}' if params else ''
        response = regular_request(
            url=f'{url}{road_map_path}{self.request_return_type}',
            cookies=self.cookies
        )
        if response.status_code == 200:
            data = self.for_normal_dict(response.text)
        else:
            logger.error(f'Bad status of response: {response.status_code}')
            data = {}
        return BaseResponse(
            data=data,
            metadata=BaseMetadata(response.status_code, response.reason)
        )

    def auth(self) -> dict:
        auth = HTTPBasicAuth(self.login, self.password)
        data = requests.get(
            url=f'{self.moex_auth_site}',
            auth=auth)
        return dict(data.cookies)


moex = Moex()
