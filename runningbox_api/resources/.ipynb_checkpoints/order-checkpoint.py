from .base import Resource
from ..constants.urls import URL


class Order(Resource):
    endpoint = URL.ORDER

    def order_service(self, data=None, **options):
        path = f'{self.endpoint}'
        return self._post(path, data, **options)