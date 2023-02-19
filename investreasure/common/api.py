import logging
import typing
import json
import requests
from requests.models import Response

from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer

from django.http import HttpResponse

from exceptions import InvestreasureException

logger = logging.getLogger('common.api')


def get_input_data(
        ins_cls: typing.Type[BaseSerializer],
        request: Request,
        **ins_cls_kwargs
):
    method = request.method
    if method in ('POST', 'PATCH'):
        req_data = request.data
    else:
        req_data = request.GET
    raise_exception = ins_cls_kwargs.pop('raise_exception', False)
    ins = ins_cls(data=req_data, **ins_cls_kwargs)
    if not ins.is_valid(raise_exception=raise_exception):
        return None
    return ins.validated_data


def get_validated_data_or_400(
        ins_cls: typing.Type[BaseSerializer],
        request: Request,
        **ins_cls_kwargs
):
    """Валидация входных параметров"""
    # Exception is handled by custom exception handler - see settings.py
    ins_cls_kwargs['raise_exception'] = True
    data = get_input_data(ins_cls, request, **ins_cls_kwargs)
    return data


def get_validated_data_or_raise(
        ins_cls: typing.Type[BaseSerializer],
        request: Request,
        **ins_cls_kwargs
):
    """Валидация входных параметров для методов МП"""
    ins_cls_kwargs['raise_exception'] = True
    try:
        data = get_input_data(ins_cls, request, **ins_cls_kwargs)
    except (ValidationError, ):
        raise
    return data


class BaseMetadata:
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

    def to_dict(self):
        resp_dict = {
            'code': self.code,
            'message': self.message
        }
        if hasattr(self, 'context'):
            resp_dict['context'] = getattr(self, 'context')
        return resp_dict


class BaseResponse:
    def __init__(self, data: dict = None, metadata: BaseMetadata = None):
        self.data = data
        self.metadata = metadata

    def to_dict(self):
        return {
            'data': self.data,
            'metadata': self.metadata.to_dict()
        }


class ResponseMixin(HttpResponse):
    # все респонсы должны быть инстансами этого класса
    def __init__(self, content=None):
        super().__init__(content=json.dumps(content, ensure_ascii=False))


def regular_request(
        url: str,
        method: str = 'GET',
        data: dict = None,
        cookies: dict = None,
) -> Response:
    """
    Regular request to site
    """
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Connection': 'close',
    }
    try:
        logger.info(f'Try to get info from {url}')
        if method.upper() == 'GET':
            resp = requests.get(url, headers=headers, cookies=cookies)
        elif method.upper() == 'POST':
            resp = requests.post(url, headers=headers, data=data, cookies=cookies)
        else:
            raise TypeError
        return resp
    except Exception as ex:
        logger.exception(f'{ex}')
        raise InvestreasureException(type='INTERNET_ERROR')


def get_params_from_dict(params_dict: dict) -> str or None:
    params = []
    for key, val in params_dict.items():
        params.append(f'{key}={val}')
    return '?' + '&'.join(params) if params else None


def get_json_from_post(request: Request):
    return json.loads(request.body)


def fields_filter(inp: list, fields: list):
    out = []
    for index, item in enumerate(inp):
        tmp = {}
        for key, val in item.items():
            if key in fields:
                tmp[key] = val
        out.append(tmp)
    return out
