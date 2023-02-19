RESPONSE_CODES_MAPPING = {
    'SUCCESS': 0,
    'INTERNET_ERROR': 1,
    'FILE_ERROR': 2,
    'DB_ERROR': 3,
    'CONFIG_ERROR': 4,
    'HTTP_ERROR': 5,
    'PARAMETERS_ERROR': 6,
    'CACHE_ERROR': 7,
    'MARKUP_ERROR': 8,
    'UNKNOWN_ERROR': 100
}


class InvestreasureException(Exception):
    """
        Custom exceptions
        Main params:
        code - RESPONSE_CODES_MAPPING
        message - error message for developer
        return_message - message for user
        """

    CODES = RESPONSE_CODES_MAPPING

    def __init__(self, *args, **kwargs):
        self.context = {
            'exception_code': self.CODES[kwargs.get('type', 'UNKNOWN_ERROR')],
        }
        for key, value in kwargs.items():
            self.context[key] = value
        super().__init__(*args)
