from aiohttp import web


# error
class HttpError(web.HTTPClientError):
    status_code = 400

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, content_type='application/json')