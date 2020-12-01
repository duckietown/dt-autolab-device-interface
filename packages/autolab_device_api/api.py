import logging

from flask import Flask
from flask_cors import CORS

from .actions.version import version as api_version
from .actions.bag.recorder.all import bar_recorder


class AutolabDeviceAPI(Flask):

    def __init__(self, debug=False):
        super(AutolabDeviceAPI, self).__init__(__name__)
        # register blueprints (/version)
        self.register_blueprint(api_version)
        # register blueprints (/bag/recorder/*)
        self.register_blueprint(bar_recorder)
        # apply CORS settings
        CORS(self)
        # configure logging
        logging.getLogger('werkzeug').setLevel(logging.DEBUG if debug else logging.WARNING)
