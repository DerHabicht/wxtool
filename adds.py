import requests
from enum import Enum, auto
from mgrs import MGRS
from typing import List
from xml.etree import ElementTree

from mission_profile import Location


BASE_URL = 'https://aviationweather.gov/adds/dataserver_current/httpparam'
MAX_DISTANCE = 20


class ReportType(Enum):
    METAR = auto()
    TAF = auto()


def _unpack_response(adds_response: str, report_type: ReportType) -> str:
    root = ElementTree.fromstring(adds_response)
    stations = [f'- {x.find("raw_text").text}' for x in root.find('data').findall(report_type.name)]

    return '\n'.join(stations)


def _get_waypoints(route: List[Location]) -> (List[str], str):
    converter = MGRS()
    waypoints = []
    routestr = ''

    for location in route:
        routestr += f'{location.coordinate} -> '
        pt = converter.toLatLon(location.coordinate)
        waypoints.append(f'{pt[1]},{pt[0]}')

    return waypoints, routestr


def get_route_metars(route: List[Location]) -> str:
    waypoints, routestr = _get_waypoints(route)

    print(f'Fetching METARs for route {routestr[:-4]}...')

    params = {
        'dataSource': 'metars',
        'requestType': 'retrieve',
        'format': 'xml',
        'flightPath': f'{MAX_DISTANCE};{";".join(waypoints)}'
    }

    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()

    return _unpack_response(r.text, ReportType.METAR)


def get_route_tafs(route: List[Location]) -> str:
    waypoints, routestr = _get_waypoints(route)

    print(f'Fetching TAFs for route {routestr[:-4]}...')

    params = {
        'datasource': 'tafs',
        'requestType': 'retrieve',
        'format': 'xml',
        'flightPath': f'{MAX_DISTANCE};{";".join(waypoints)}'
    }

    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()

    return _unpack_response(r.text, ReportType.TAF)
