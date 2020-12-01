import datetime
import os
import subprocess
import time

from flask import Blueprint

from autolab_device_api.constants import BAG_RECORDER_DIR, BAG_RECORDER_MAX_DURATION_SECS
from autolab_device_api.utils import response_ok, response_error
from autolab_device_api.knowledge_base import KnowledgeBase

from dt_device_utils import get_device_hostname


bag_recorder = Blueprint('bag_recorder', __name__)
_GRP = "bag/recorder"


@bag_recorder.route('/bag/recorder/start')
def _bag_recorder_start():
    # make sure target directory exists
    subprocess.run(["mkdir", "-p", BAG_RECORDER_DIR])

    bag_name = f"{datetime.datetime.now().isoformat('|')}.bag"
    # if all topics, put "--all" in the list
    topics = ["--all"]

    if len(topics) == 0:
        return response_error("no topic is specified so no bag is recorded")

    cmd = [
        "rosbag",
        "record",
        f"--output-name={os.path.join(BAG_RECORDER_DIR, bag_name)}",
        f"--duration={BAG_RECORDER_MAX_DURATION_SECS}",
    ] + topics

    proc = subprocess.Popen(cmd)
    KnowledgeBase.set(_GRP, bag_name, proc)
    # return current API bag_recorder
    return response_ok({'bag_name': bag_name})


@bag_recorder.route('/bag/recorder/stop/<string:bag_name>')
def _bag_recorder_stop(bag_name: str):
    proc = KnowledgeBase.get(_GRP, bag_name, None)
    if proc is None:
        return response_error(f"No bag with name {bag_name} is being recorded")
    # stop recording
    proc.terminate()
    time.sleep(1)
    # verify stopped
    try:
        assert(not proc.poll() is None)
    except:
        return response_error("Could not stop bag recording")

    # return current API bag_recorder
    return response_ok({
        'local_path': os.path.join(BAG_RECORDER_DIR, bag_name),
        'url': f'http://{get_device_hostname()}.local/files/logs/bags/{bag_name}'
    })
