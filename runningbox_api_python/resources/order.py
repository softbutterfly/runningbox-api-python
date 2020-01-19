from ..errors import NotAllowed
from .base import Resource


class Order(Resource):
    endpoint = "https://runningboxapi.azurewebsites.net/api/orden/"
    price_estimate_endpoint = "http://croiii.azurewebsites.net/home/GetCalculo"

    def create(self, data, **options):
        data.update(
            {"clave_api": self.client.api_key, "ruc_broker": self.client.broker_tax_id,}
        )
        data = dict((k.upper(), v) for k, v in data.items())

        return super().create(data, **options)

    def list(self, data=None, **options):
        raise NotAllowed("You can't perform this action.")

    def read(self, id_, data=None, **options):
        raise NotAllowed("You can't perform this action.")

    def update(self, id_, data=None, **options):
        raise NotAllowed("You can't perform this action.")

    def delete(self, id_, data=None, **options):
        raise NotAllowed("You can't perform this action.")

    def estimate(self, data, **options):
        data.update(
            {"clave_api": self.client.api_key,}
        )

        path = "{0}".format(self.price_estimate_endpoint)
        return self._get(path, data, **options)

    def tracking(self, id_, data=None, **options):
        """ Call to tracking endpoint. Here `id_` param can be the number of
        service order [NRO_OS] returned by the create method or the order
        number [NRO_PEDIDO] sent in the create method.
        """
        path = "{0}/Get/{1}/{2}".format(self.endpoint, id_, self.client.api_key)
        return self._get(path, data, **options)
