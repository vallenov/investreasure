import logging
import sys

from rest_framework.views import APIView

# import investreasure.index.serializers as cs
# import investreasure.index.models as cms

logger = logging.getLogger('index')


class IndexAllView(APIView):

    def get(self, request):
        """
        Определение качества звонка
        """
        response = dict()
        try:
            response = {
                'test': 'OK'
            }
        except Exception as exc:
            logger.exception(f'Failed get call quality: {exc}')
        finally:
            exc_info = sys.exc_info()
            if exc_info[0] is not None:
                logger.exception(f"{request.path} has failed")
            return response
