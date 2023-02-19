import logging
import sys

from rest_framework.views import APIView

from common.api import (
    ResponseMixin,
    get_params_from_dict,
    get_json_from_post,
    fields_filter,
)
from moex.moex import moex
from exceptions import InvestreasureException

logger = logging.getLogger('history')


class MOEXHistoryView(APIView):

    def post(self, request):
        """
        Получение всех направлений мониторинга
        """
        response = None
        try:
            input_json = get_json_from_post(request)
            params = get_params_from_dict(input_json.get('get_params'))
            response = moex.moex_request(
                road_map_path=moex.road_map['history'][request.path.split('/')[-1]],
                params=params
            )
            fields = input_json.get('fields')
            if fields:
                response.data['history'] = fields_filter(response.data['history'], fields)
        except InvestreasureException as ite:
            response.metadata.context = ite.context
        except Exception as exc:
            logger.exception(f'Failed get call quality: {exc}')
        finally:
            exc_info = sys.exc_info()
            if exc_info[0] is not None:
                logger.exception(f"{request.path} has failed")
            return ResponseMixin(response.to_dict())
