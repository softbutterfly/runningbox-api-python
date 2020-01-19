import json
from types import ModuleType

from requests import session

from . import resources
from .constants import HttpStatusCode
from .errors import BadRequestError, GatewayError, ServerError
from .utils import capitalize_camel_case
from .version import VERSION

RESOURCE_CLASSES = {}

for name, module in resources.__dict__.items():
    capitalized_name = capitalize_camel_case(name)
    is_module = isinstance(module, ModuleType)
    is_in_module = capitalized_name in getattr(module, "__dict__", {})

    if is_module and is_in_module:
        RESOURCE_CLASSES[name] = module.__dict__[capitalized_name]


class Client:
    base_url = None

    def __init__(self, api_key, broker_tax_id):
        """Initialize a Client object with session, optional auth handler,
        and options"""
        self.api_key = api_key
        self.broker_tax_id = broker_tax_id
        self.session = session()

        self._set_client_headers()

        for name, klass in RESOURCE_CLASSES.items():
            setattr(self, name, klass(self))

    @staticmethod
    def _get_version():
        return ".".join(VERSION)

    @staticmethod
    def _get_error_message(response):
        msg = ""
        json_response = response.json()

        if "error" in json_response:
            if isinstance(json_response["error"], str):
                msg = json_response["error"]

            elif "message" in json_response["error"]:
                msg = json_response["error"]["message"]

        return msg

    def _get_error(self, response):
        msg = self._get_error_message(response)
        errors = {
            HttpStatusCode.BAD_REQUEST_ERROR: BadRequestError,
            HttpStatusCode.SERVER_ERROR: ServerError,
            HttpStatusCode.GATEWAY_ERROR: GatewayError,
            "default": ServerError,
        }

        if response.status_code in errors:
            return errors[response.status_code](msg)

        return errors["default"](msg)

    def _set_client_headers(self):
        self.session.headers.update(
            {
                "User-Agent": "Runningbox-API-Python/{0}".format(self._get_version()),
                "Content-type": "application/json",
                "Accept": "application/json",
            }
        )

    def _update_request(self, data, options):
        """Updates the resource data and header options."""
        data = json.dumps(data)

        if "headers" not in options:
            options["headers"] = {}

        options["headers"].update(
            {
                "User-Agent": "Runningbox-API-Python/{0}".format(self._get_version()),
                "Content-type": "application/json",
                "Accept": "application/json",
            }
        )

        return data, options

    def request(self, method, path, **options):
        """Dispatches a request to the Running Box HTTP API."""
        url = path

        response = getattr(self.session, method)(url, **options)

        if HttpStatusCode.OK <= response.status_code < HttpStatusCode.REDIRECT:
            return {"status": response.status_code, "data": response.json()}

        raise self._get_error(response)

    def get(self, path, params, **options):
        """Parses GET request options and dispatches a request."""
        return self.request("get", path, params=params, **options)

    def post(self, path, data, **options):
        """Parses POST request options and dispatches a request."""
        data, options = self._update_request(data, options)
        return self.request("post", path, data=data, **options)

    def patch(self, path, data, **options):
        """Parses PATCH request options and dispatches a request."""
        data, options = self._update_request(data, options)
        return self.request("patch", path, data=data, **options)

    def delete(self, path, data, **options):
        """Parses DELETE request options and dispatches a request."""
        data, options = self._update_request(data, options)
        return self.request("delete", path, data=data, **options)

    def put(self, path, data, **options):
        """Parses PUT request options and dispatches a request."""
        data, options = self._update_request(data, options)
        return self.request("put", path, data=data, **options)
