import requests
from mgrs import MGRS
from typing import List
from xml.etree import ElementTree

from mission_profile import Location


BASE_URL = 'https://aviationweather.gov/adds/dataserver_current/httpparam'
MAX_DISTANCE = 20


def unpack_metars(adds_response: str) -> str:
    root = ElementTree.fromstring(adds_response)
    # metars = [
    #     {
    #         'station': x.find('station_id').text,
    #         'time': x.find('observation_time').text,
    #         'raw_text': x.find('raw_text').text,
    #     }
    #     for x in root.find('data').findall('METAR')
    # ]

    # station_ids = set()
    # stations = []
    # for metar in metars:
    #     if metar['station'] not in station_ids:
    #         station_ids.add(metar['station'])
    #         stations.append(f'    {metar["raw_text"]}')
    stations = [f'- {x.find("raw_text").text}' for x in root.find('data').findall('METAR')]

    return '\n'.join(stations)


def get_route_metars(route: List[Location]) -> str:
    converter = MGRS()
    waypoints = []
    routestr = ''

    for location in route:
        routestr += f'{location.coordinate} -> '
        pt = converter.toLatLon(location.coordinate)
        waypoints.append(f'{pt[1]},{pt[0]}')

    print(f'Fetching METARs for route {routestr[:-4]}...')

    params = {
        'dataSource': 'metars',
        'requestType': 'retrieve',
        'format': 'xml',
        'flightPath': f'{MAX_DISTANCE};{";".join(waypoints)}'
    }

    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()

    return unpack_metars(r.text)