import io

from requests.adapters import BaseAdapter
from requests.models import Response
from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers

try:
    from http.client import responses
except ImportError:
    from httplib import responses

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class Content(object):

    def __init__(self, content):
        self._len = len(content)
        self._read = 0
        self._bytes = io.BytesIO(content)

    def __len__(self):
        return self._len

    def read(self, amt=None):
        if amt:
            self._read += amt
        return self._bytes.read(amt)

    def stream(self, amt=None, decode_content=None):
        while self._read < self._len:
            yield self.read(amt)

    def release_conn(self):
        pass


class WSGIAdapter(BaseAdapter):
    server_protocol = 'HTTP/1.1'
    wsgi_version = (1, 0)

    def __init__(self, app, multiprocess=False, multithread=False, run_once=False):
        self.app = app
        self.multiprocess = multiprocess
        self.multithread = multithread
        self.run_once = run_once
        self.errors = io.BytesIO()

    def send(self, request, *args, **kwargs):
        urlinfo = urlparse(request.url)

        data = request.body.encode('utf-8') if request.body else b''

        environ = {
            'CONTENT_TYPE': request.headers.get('Content-Type', 'text/plain'),
            'CONTENT_LENGTH': len(data),
            'PATH_INFO': urlinfo.path,
            'REQUEST_METHOD': request.method,
            'SERVER_NAME': urlinfo.hostname,
            'SERVER_PORT': urlinfo.port or (443 if urlinfo.scheme == 'https' else 80),
            'SERVER_PROTOCOL': self.server_protocol,
            'wsgi.version': self.wsgi_version,
            'wsgi.url_scheme': urlinfo.scheme,
            'wsgi.input': Content(data),
            'wsgi.errors': self.errors,
            'wsgi.multiprocess': self.multiprocess,
            'wsgi.multithread': self.multithread,
            'wsgi.run_once': self.run_once,
            'wsgi.url_scheme': urlinfo.scheme,
        }

        environ.update({
            'HTTP_{}'.format(name).replace('-', '_').upper(): value
            for name, value in request.headers.items()
        })

        response = Response()

        def start_response(status, headers):
            response.status_code = int(status.split(' ')[0])
            response.reason = responses.get(response.status_code, 'Unknown Status Code')
            response.headers = CaseInsensitiveDict(headers)
            response.encoding = get_encoding_from_headers(response.headers)

        response.request = request
        response.url = request.url

        response.raw = Content(b''.join(self.app(environ, start_response)))

        return response

    def close(self):
        pass
