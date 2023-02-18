from settings import (
    MAIN_URL,
    REQUEST_RETURN_TYPE,
)
from common.api import regular_request


class Moex:

    site = MAIN_URL
    request_return_type = REQUEST_RETURN_TYPE

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

    def index(self):
        data = regular_request(f'{self.site}/index.{self.request_return_type}')
        return self.for_normal_dict(data)


moex = Moex()
