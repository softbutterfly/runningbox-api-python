from .stages import Stage

class URL:
    PREFIX = {
        #Stage.PRODUCTION: 'api',
        Stage.RUNNING_BOX_API: 'runningboxapi',
        Stage.CROIII: 'croiii',
        Stage.TEST: 'stageapi',
    }

    BASE_FORMAT = "https://{prefix}.azurewebsites.net"
    ORDER_URL = "https://runningboxapi.azurewebsites.net/api/orden/"
    RATE_URL = "https://croiii.azurewebsites.net/home/GetCalculo"
    TRACKING_URL = "http://runningboxapi.azurewebsites.net/api/orden/Get/{}/{}"