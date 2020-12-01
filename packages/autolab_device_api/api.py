import logging
import os

from enum import Enum

from flask import Flask
from flask_cors import CORS

from .actions.version import version as api_version
from .actions.bag.recorder.all import bag_recorder
from .actions.car.estop.all import car_estop


class AutolabDeviceAPI(Flask):

    def __init__(self, debug=False):
        super(AutolabDeviceAPI, self).__init__(__name__)

        # config for which robot types, a certain api is enabled
        class RobotType(Enum):
            duckiebot = 1
            watchtower = 2
            duckietown = 3

            @classmethod
            def lst_all(cls):
                return list(cls)

        # self robot type
        robot_type = RobotType[os.environ["ROBOT_TYPE"]]

        # blueprint: lst_target_robot_types
        api_filter = {
            # (/version)
            api_version: RobotType.lst_all(),

            # (/bag/recorder/*)
            bag_recorder: [
                RobotType.duckiebot,
                RobotType.watchtower
            ],

            # (/car/estop/*)
            car_estop: [
                RobotType.duckiebot
            ],
        }

        # if self robot type is a target, enable the api
        for blueprint, targets in api_filter.items():
            if robot_type in targets:
                # register blueprints
                self.register_blueprint(blueprint)

        # apply CORS settings
        CORS(self)
        # configure logging
        logging.getLogger('werkzeug').setLevel(
            logging.DEBUG if debug else logging.WARNING)
