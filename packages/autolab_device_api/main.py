import sys
from dt_class_utils import DTProcess, AppStatus

from code_api.api import AutolabDeviceAPI

CODE_API_PORT = 9091


class AutolabDeviceAPIApp(DTProcess):
    
    def __init__(self):
        super(AutolabDeviceAPIApp, self).__init__('AutolabDeviceAPI')
        self._api = AutolabDeviceAPI(debug=self.is_debug)
        self.status = AppStatus.RUNNING
        # register shutdown callback
        self.register_shutdown_callback(_kill)
        # serve HTTP requests over the REST API
        self._api.run(host='0.0.0.0', port=CODE_API_PORT)


def _kill():
    sys.exit(0)


if __name__ == '__main__':
    app = AutolabDeviceAPIApp()
