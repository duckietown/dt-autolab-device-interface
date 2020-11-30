import logging

from flask import Flask
from flask_cors import CORS

from .actions.version import version as api_version


class AutolabDeviceAPI(Flask):

    def __init__(self, debug=False):
        super(AutolabDeviceAPI, self).__init__(__name__)
        # register blueprints (/*)
        self.register_blueprint(api_version)
        # apply CORS settings
        CORS(self)
        # configure logging
        logging.getLogger('werkzeug').setLevel(logging.DEBUG if debug else logging.WARNING)
