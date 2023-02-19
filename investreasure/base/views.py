import logging
import sys

from rest_framework.views import APIView

from common.api import (
    ResponseMixin,
)
from moex.moex import moex

logger = logging.getLogger('index')


class MOEXBaseView(APIView):

    def get(self, request):
        """
        Получение всех направлений мониторинга
        """
        response = None
        try:
            response = moex.moex_request(
                road_map_path=moex.road_map['base'][request.path.split('/')[-1]]
            )
        except Exception as exc:
            logger.exception(f'Failed get call quality: {exc}')
        finally:
            exc_info = sys.exc_info()
            if exc_info[0] is not None:
                logger.exception(f"{request.path} has failed")
            return ResponseMixin(response.to_dict())
