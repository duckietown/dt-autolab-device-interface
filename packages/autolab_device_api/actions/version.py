from flask import Blueprint

from autolab_device_api.constants import API_VERSION
from autolab_device_api.utils import response_ok


version = Blueprint('version', __name__)


@version.route('/version')
def _version():
    # return current API version
    return response_ok({'version': API_VERSION})
