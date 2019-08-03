from .base import Resource
from ..constants.urls import URL

class Tracking(Resource):
    endpoint = URL.TRACKING_URL

    def tracking_service(self,data=None,**options):
        url_tracking = self.endpoint.format(data['NRO_PEDIDO'],data['CLAVE_API'])
        return self._get(url_tracking, data, **options)