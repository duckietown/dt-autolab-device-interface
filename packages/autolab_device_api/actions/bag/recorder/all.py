import datetime
import subprocess

from flask import Blueprint

import rosbag

from autolab_device_api.constants import API_VERSION, MAX_BAG_DURATION_SECS
from autolab_device_api.utils import response_ok, response_error
from autolab_device_api.knowledge_base import KnowledgeBase

from dt_device_utils import get_device_hostname


bar_recorder = Blueprint('bar_recorder', __name__)


@bar_recorder.route('/bag/recorder/start')
def _bar_recorder_start():
    bagname = ""
    proc = subprocess.Popen(['rosbag', 'record', f'--output-name={bagname}', f'--duration={MAX_BAG_DURATION_SECS}', '--all'])
    KnowledgeBase.set("bag/recorder", bagname, proc)
    # return current API bar_recorder
    return response_ok({'bagname': bagname})


@bar_recorder.route('/bag/recorder/stop/<str:bag_name>')
def _bar_recorder_stop(bag_name: str):
    proc = KnowledgeBase.get("bag/recorder", bag_name, None)
    if proc is None:
        return response_error(f"No bag with name {bag_name}")
    # stop it
    proc.kill()
    # return current API bar_recorder
    return response_ok({
        'local_path': f'/data/logs/bags/{bag_name}.bag',
        'url': f'http://{get_device_hostname()}.local/files/logs/bags/{bag_name}.bag'
    })
