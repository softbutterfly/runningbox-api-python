import json
from requests import session
from base64 import b64encode
from types import ModuleType
from .utils import capitalize_camel_case
from .constants import Stage, URL, HttpStatusCode, ErrorCode
from .errors import BadRequestError, GatewayError, ServerError
from .version import VERSION
from . import resources

RESOURCE_CLASSES = {}

for name, module in resources.__dict__.items():
    if isinstance(module, ModuleType) and capitalize_camel_case(name) in module.__dict__:
        RESOURCE_CLASSES[name] = module.__dict__[capitalize_camel_case(name)]

class Client:
    base_url = None

    def __init__(self,api_key,api_secret):
        """Initialize a Client object with session, optional auth handler,
        and options"""
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = session()

        self._set_auth_string()
        self._set_client_headers()

        for name, klass in RESOURCE_CLASSES.items():
            setattr(self, name, klass(self))

    def _set_auth_string(self):
        raw_auth_string = f'{self.api_key}:{self.api_secret}'.encode('utf-8')
        self.auth_string = b64encode(raw_auth_string).decode('utf-8')

    def _set_client_headers(self):
        self.session.headers.update({
            'User-Agent': f'runningbox-api',
            'Authorization': f'Basic {self.auth_string}',
            'Content-type': 'application/json',
            'Accept': 'application/json'
        })

    def request(self, method, path, **options):
        """Dispatches a request to the RUNNING HTTP API."""

        url = path

        response = getattr(self.session, method)(url, **options)
        if HttpStatusCode.OK <= response.status_code < HttpStatusCode.REDIRECT:
            return {
                'status': response.status_code,
                'data': response.json()
            }

        else:
            msg = ""
            code = ""
            json_response = response.json()
            if 'error' in json_response:
                if isinstance(json_response['error'], str):
                    msg = json_response['error']

                if 'message' in json_response['error']:
                    msg = json_response['error']['message']

            if str.upper(code) == ErrorCode.BAD_REQUEST_ERROR:
                raise BadRequestError(msg)
            elif str.upper(code) == ErrorCode.GATEWAY_ERROR:
                raise GatewayError(msg)
            elif str.upper(code) == ErrorCode.SERVER_ERROR:
                raise ServerError(msg)
            else:
                raise ServerError(msg)

    def get(self, path, params, **options):
        """Parses GET request options and dispatches a request."""
        return self.request('get', path, params=params, **options)

    def post(self, path, data, **options):
        """Parses POST request options and dispatches a request."""
        data, options = self._update_request(data, options)
        return self.request('post', path, data=data, **options)

    def patch(self, path, data, **options):
        """Parses PATCH request options and dispatches a request."""
        data, options = self._update_request(data, options)
        return self.request('patch', path, data=data, **options)

    def delete(self, path, data, **options):
        """Parses DELETE request options and dispatches a request."""
        data, options = self._update_request(data, options)
        return self.request('delete', path, data=data, **options)

    def put(self, path, data, **options):
        """Parses PUT request options and dispatches a request."""
        data, options = self._update_request(data, options)
        return self.request('put', path, data=data, **options)

    def _update_request(self, data, options):
        """Updates The resource data and header options."""
        data = json.dumps(data)

        if 'headers' not in options:
            options['headers'] = {}

        options['headers'].update({'Content-type': 'application/json'})

        return data, options