import logging
import sys

from rest_framework.views import APIView

from common.api import (
    ResponseMixin,
    regular_request,
)
from settings import (
    MAIN_URL,
    REQUEST_RETURN_TYPE
)

logger = logging.getLogger('index')


class IndexAllView(APIView):

    def get(self, request):
        """
        Получение всех направлений мониторинга
        """
        response = dict()
        try:
            raw_data = regular_request(f'{MAIN_URL}/index.{REQUEST_RETURN_TYPE}')
            for key, val in raw_data.items():
                if key == 'metadata':
                    continue
                response[key] = []
                for data in val['data']:
                    row = dict(zip(val['columns'], data))
                    response[key].append(row)
        except Exception as exc:
            logger.exception(f'Failed get call quality: {exc}')
        finally:
            exc_info = sys.exc_info()
            if exc_info[0] is not None:
                logger.exception(f"{request.path} has failed")
            return ResponseMixin(response)
