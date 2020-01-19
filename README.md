[![Python Versions](https://img.shields.io/pypi/pyversions/runningbox-api-python.svg?color=3776AB&logo=python&logoColor=white)](https://www.python.org/)
[![PyPI Version](https://img.shields.io/pypi/v/runningbox-api-python.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/runningbox-api-python/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/runningbox-api-python.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/runningbox-api-python/)

[![Build Status](https://travis-ci.org/softbutterfly/runningbox-api-python.svg?branch=master)](https://travis-ci.org/softbutterfly/runningbox-api-python)
[![codecov](https://codecov.io/gh/softbutterfly/runningbox-api-python/branch/master/graph/badge.svg)](https://codecov.io/gh/softbutterfly/runningbox-api-python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/710bffdc3057465aa7368ebd182b11ed)](https://www.codacy.com/gh/softbutterfly/runningbox-api-python?utm_source=github.com&utm_medium=referral&utm_content=softbutterfly/runningbox-api-python&utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/710bffdc3057465aa7368ebd182b11ed)](https://www.codacy.com/gh/softbutterfly/runningbox-api-python?utm_source=github.com&utm_medium=referral&utm_content=softbutterfly/runningbox-api-python&utm_campaign=Badge_Coverage)

[![Stars](https://img.shields.io/github/stars/softbutterfly/runningbox-api-python?logo=github)](https://github.com/softbutterfly/runningbox-api-python/)
[![License](https://img.shields.io/pypi/l/runningbox-api-python.svg?color=blue)](https://github.com/softbutterfly/runningbox-api-python/blob/master/LICENSE.txt)

# Running Box Python API

Estimate, create, and track your Running Box orders trough their API.

## Requirements

This package requires at least

- requests 2.21.0
- python 3.7

This package was not tested with prior versions of these packages but it can works as well.

## Install

You can install via pip. Run the following command:

```
$ pip install runningbox-api-python
```

## Credentials

Get in touch with [Runningbox](http://runningbox.pe/) and request your account.
They will give you an `API_KEY` asociated to your tax id (`BROKER_TAX_ID`).

Example `API_KEY` & `BROKER_TAX_ID`:

```python
api_key = 'XiX7X46D4rKyCy6pGOCLOg=='
broker_tax_id = '123456790'
```

## Usage

Simple usage looks like:

### Initialize client

```python
from runningbox_api_python.client import Client

api_key = 'sample_api_key'
broker_tax_id = 'sample_broker_tax_id'

client = Client(apapi_key, apbroker_tax_id)
```

### Estimate order price

```python
from runningbox_api_python.constants import Service

estimated_order_price = client.order.estimate(
    {
        'ubigeo': '150131',   # Ubigeo code acording to INEI
        'servicio': Service.EXPRESS,   # Service type
        'peso': '43.00'   # Weight of your package
    }
)
print(estimates_order_price)
# Will show this
# {
#     'status': 200,
#     'data': 55.4
# }
```

**Note**

- The value under 'data' label is the price in PEN

### Create order

```python
placed_order = client.order.create({
    # Cliente de envio
    "cliente": "Customer Inc.",
    "cliente_ruc": "20601826535",
    "nro_pedido": "CUSTOMER-d98b73bffdd54685a3c40c544a539668",
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
})

print(placed_order)
# Will show this
# {
#     'status': 200,
#     'data': {
#         'ID_OS': 408453,
#         'NRO_ORDEN': '1000362049',
#         'ID_RSPTA': 71,
#         'DES_RSPTA': 'CREADO',
#         'FECHA': '11/24/2019 2:39:29 AM'
#     }
# }
```

### Get order tracking

Order tracking can be done with `nro_pedido` parameter that you used to create your order.

```python
request_number = 'CUSTOMER-d98b73bffdd54685a3c40c544a539668'
tracking = client.order.tracking(request_number)
print(tracking)
# Will show this
# {
#     'status': 200,
#     'data': [
#         {
#             'NRO_OS': '1000362049',
#             'CLIENTE': 'Customer Inc.',
#             'ID_CPOINT': '71',
#             'DES_CPOINT': 'CREADO',
#             'FECHA': '24/11/2019',
#             'HORA': '02:39:29',
#             'OBSERVACION': ''
#         }
#     ]
# }
```

Or with `nro_orden` parameter that you get after create your order.

```python
order_number = '1000362049'
tracking = client.order.tracking(order_number)
print(tracking)
# Will show this
# {
#     'status': 200,
#     'data': [
#         {
#             'NRO_OS': '1000362049',
#             'CLIENTE': 'Customer Inc.',
#             'ID_CPOINT': '71',
#             'DES_CPOINT': 'CREADO',
#             'FECHA': '24/11/2019',
#             'HORA': '02:39:29',
#             'OBSERVACION': ''
#         }
#     ]
# }
```

**Note**

- The value under 'data' label is a list of events that take place in the delivery process.
