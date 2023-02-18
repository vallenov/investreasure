import logging
import typing
import json
import requests

from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer

from django.http import HttpResponse

logger = logging.getLogger('index')


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


class ResponseMixin(HttpResponse):
    # все респонсы должны быть инстансами этого класса
    def __init__(self, content=None):
        super().__init__(content=json.dumps(content, ensure_ascii=False))


def regular_request(
        url: str,
        method: str = 'GET',
        data: dict = None,
        cookies: dict = None,
) -> dict:
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
        if resp.status_code == 200:
            resp = json.loads(resp.text)
            logger.info(f'Get successful')
            return resp
        else:
            logger.error(f'Bad status of response: {resp.status_code}')
    except Exception as ex:
        logger.exception(f'{ex}')


def get_params_from_request(request: Request) -> str or None:
    params = []
    for key, val in request.query_params.items():
        params.append(f'{key}={val}')
    return '?' + '&'.join(params) if params else None
