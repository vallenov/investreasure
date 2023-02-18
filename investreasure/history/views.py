import logging
import sys

from rest_framework.views import APIView

from common.api import (
    ResponseMixin,
    get_params_from_request
)
from moex.moex import moex

logger = logging.getLogger('history')


class MOEXHistoryView(APIView):

    def get(self, request):
        """
        Получение всех направлений мониторинга
        """
        response = dict()
        try:
            params = get_params_from_request(request)
            response = moex.moex_request(
                road_map_path=moex.road_map['history'][request.path.split('/')[-1]],
                params=params
            )
        except Exception as exc:
            logger.exception(f'Failed get call quality: {exc}')
        finally:
            exc_info = sys.exc_info()
            if exc_info[0] is not None:
                logger.exception(f"{request.path} has failed")
            return ResponseMixin(response)