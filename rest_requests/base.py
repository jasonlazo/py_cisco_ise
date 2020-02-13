from http import HTTPStatus


class CiscoIseRequest:

    def __init__(self, path, method, ok_status_code=HTTPStatus.OK, body=None):
        self.path = path
        self.method = method
        self.ok_status_code = ok_status_code
        self._body = body if body else {}

    @property
    def body(self):
        return {**self._body, **{}}