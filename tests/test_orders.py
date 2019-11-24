import os
import unittest
from uuid import uuid4

from dotenv import load_dotenv

from runningbox_api_python import __version__
from runningbox_api_python.client import Client
from runningbox_api_python.resources import Order
from runningbox_api_python.constants import Service


class OrdersTest(unittest.TestCase):
    order_data_for_estimate = {  # pylint: disable=E1101
        'ubigeo': '150131',
        'servicio': 'EXPRESS',
        'peso': '43.00'
    }
    order_data_for_create = {
        # Cliente de envio
        "cliente": "Customer Inc.",
        "cliente_ruc": "20601826535",
        "piezas": "10",
        "imp_seguro": "",
        "descripcion": "Sample description",
        "peso": "10.0",
        "cod": "",
        "dd": "",
        "importe_cod": "0.00",
        "servicio": Service.EXPRESS,

        # Cliente final
        "cliente_final": "Jhon Doe",
        "tipo_doc": "1",
        "numero_doc": "123456789",

        # "documento1": "",
        # "nrodoc1":"",
        # "documento2":"",
        # "nrodoc2":"",
        # "documento3":"",
        # "nrodoc3":"",
        # "documento4":"",
        # "nrodoc4":"",

        # Entrega
        "ubigeo": "150101",
        "departamento": "Lima",
        "provincia": "Lima",
        "distrito": "Lima",
        "direccion": "jr la mar 1000",
        "observacion": "",
        "mail": "jhon.doe@example.com",
        "telefono": "999999999",
        "contacto": "Margery Doe (999999998)",

        # Recojo
        "nombre_resp_almacen": "Donnald Doe (999999997)",
        "dni_resp_almacen": "123456788",
        "telefono_resp_almacen": "999999997",
        "arco_resp_almacen": "8:00 - 19:00",
        "direccion_almacen": "Sample Address 777, No where.",
        "ubigeo_almacen": "150132",
        "flag_inversa": 0,
        "flag_canal": 1,
        "notas": "",
        "productos": [
            {
                "nombre": "delirium - bvd hombre addiction - talla : xl - color : azul y negro",
                "descripcion": "delirium-bvd-hombre-addiction-1-018171",
                "sku": "dbh-add-blrj-xl",
                "peso": 10
            }
        ]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()
        self.version = __version__

        self.api_key = os.environ.get(
            'API_KEY',
            'sample_api_key'
        )

        self.broker_tax_id = os.environ.get(
            'BROKER_TAX_ID',
            'sample_api_secret'
        )

        self.request_number = f"CUSTOMER-{uuid4().hex}"
        self.order_number = None
        self.client = Client(self.api_key, self.broker_tax_id)

    def test_order_attribute_type(self):
        order = getattr(self.client, 'order', None)

        assert isinstance(order, Order)

    def test_order_client(self):
        order = getattr(self.client, 'order', None)
        assert order.client == self.client

    def test_order_estimate_status_code(self):
        response = self.client.order.estimate(  # pylint: disable=E1101
            self.order_data_for_estimate)
        assert response['status'] == 200

    def test_order_create_status_code(self):
        self.order_data_for_create.update({
            "nro_pedido": self.request_number
        })
        response = self.client.order.create(  # pylint: disable=E1101
            self.order_data_for_create)
        assert response['status'] == 200
        self.order_number = response['data']['NRO_ORDEN']

    def test_order_tracking_status_code_with_request_number(self):
        response = self.client.order.tracking(  # pylint: disable=E1101
            self.request_number)
        assert response['status'] == 200

    def test_order_tracking_status_code_with_order_number(self):
        response = self.client.order.tracking(  # pylint: disable=E1101
            self.order_number)
        assert response['status'] == 200

    def test_order_trackin_compare_order_number_and_request_number(self):
        request_number_response = self.client.order.tracking(  # pylint: disable=E1101
            self.request_number)

        order_number_response = self.client.order.tracking(  # pylint: disable=E1101
            self.order_number)

        assert request_number_response == order_number_response


if __name__ == '__main__':
    unittest.main()
