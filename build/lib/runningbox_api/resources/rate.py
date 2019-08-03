from .base import Resource
from ..constants.urls import URL


class Rate(Resource):
    endpoint = URL.RATE_URL

    def rate_service(self, data=None, **options):
        return self._get(self.endpoint, data, **options)