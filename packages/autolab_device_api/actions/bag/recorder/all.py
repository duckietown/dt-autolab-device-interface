from flask import Blueprint

import rosbag

from autolab_device_api.constants import API_VERSION
from autolab_device_api.utils import response_ok

from dt_device_utils import get_device_hostname


bar_recorder = Blueprint('bar_recorder', __name__)


@bar_recorder.route('/bag/recorder/start')
def _bar_recorder_start():
    # return current API bar_recorder
    return response_ok({'bar_recorder': API_VERSION})


@bar_recorder.route('/bag/recorder/stop')
def _bar_recorder_stop():
    bagname = 'XYZ'
    # return current API bar_recorder
    return response_ok({
        'local_path': f'/data/logs/bags/{bagname}.bag',
        'url': f'http://{get_device_hostname()}.local/files/logs/bags/{bagname}.bag'
    })
