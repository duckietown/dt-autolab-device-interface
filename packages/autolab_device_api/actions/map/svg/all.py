from flask import Blueprint
from flask import request

import logging
import os
import subprocess
import urllib.request 
import yaml

from autolab_device_api.constants import MAP_SVG_DIR
from autolab_device_api.utils import response_ok, response_error

from dt_device_utils import get_device_hostname

from duckietown_world.resources import list_maps
from duckietown_world.svg_drawing.draw_maps import draw_map
from duckietown_world.world_duckietown import load_map, construct_map


map_svg_draw = Blueprint('map_svg_draw', __name__)


def _draw_map(map_obj, map_name):
    logging.info("Start drawing...")
    # make sure target directory exists
    subprocess.run(["mkdir", "-p", MAP_SVG_DIR])

    default_map_path = os.path.join(MAP_SVG_DIR, "drawing.svg")
    map_path = os.path.join(MAP_SVG_DIR, map_name+".svg")
    try:
        draw_map(MAP_SVG_DIR, map_obj)
        os.rename(default_map_path, map_path)
    except:
        return response_error(f"Could not draw the map [{map_name}] " + 
            f"at {map_path}")


    url = f"http://{get_device_hostname()}.local/files/" + \
        map_path.strip("/data")

    return response_ok({
        'path_on_robot': map_path,
        'download_url': url,
    })



@map_svg_draw.route('/map/svg/name/<string:map_name>')
def _map_svg_draw_from_name(map_name: str):
    logging.info(f"Drawing by map name: {map_name}")

    if not map_name in list_maps():
        return response_error(f"Named map not found: {map_name}")
    else:
        return _draw_map(load_map(map_name), map_name)


@map_svg_draw.route('/map/svg/url')
def _map_svg_draw_from_url():
    """
    custom map yaml url
    """

    map_yaml_url = request.args.get("url")

    logging.info(f"Drawing by map yaml url: {map_yaml_url}")

    try:
        logging.info("Downloading map yaml file...")
        res = urllib.request.urlopen(map_yaml_url)
    except:
        return response_error(f"Invalid url: {map_yaml_url}")

    try:
        response_data = res.read()
        map_yaml = yaml.load(response_data, Loader=yaml.SafeLoader)
        logging.info("Constructing map object from downloaded map yaml...")
        map_obj = construct_map(map_yaml)
    except:
        return response_error("Could not construct map object " +
            f"from the map file at url: {map_yaml_url}")

    map_name = map_yaml_url.split('/')[-1].split('.')[0]
    return _draw_map(map_obj, map_name)
