from flask import Blueprint

import logging
import subprocess

from autolab_device_api.utils import response_ok, response_error
from dt_device_utils import get_device_hostname

car_estop = Blueprint('car_estop', __name__)


def _car_estop(on_off: bool):
    # command to run
    # rostopic pub /[HOSTNAME]/wheels_driver_node/emergency_stop duckietown_msgs/BoolStamped -1 "{header: auto, data: false}"

    topic = f"/{get_device_hostname()}/wheels_driver_node/emergency_stop"
    msg_type = "duckietown_msgs/BoolStamped"
    msg = "{header: auto, data: %s}" % on_off
    opts = [
        # publish once and exit
        "-1",
    ]
    # TODO: "-1" publishes in latching mode, so 3 seconds waited, consider rate mode and kill after certain time

    cmd = ["rostopic", "pub", topic, msg_type, msg] + opts

    # wait until finish, capture error if any
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        logging.debug(e.output)
        return response_error(e.output)

    return response_ok({"estop_engaged": on_off})


@car_estop.route('/car/estop/on')
def _car_estop_start():
    # return current API car_estop
    return _car_estop(True)


@car_estop.route('/car/estop/off')
def _car_estop_stop():
    # return current API car_estop
    return _car_estop(False)
