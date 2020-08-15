import requests
from mgrs import MGRS

from mission_profile import Location


BASE_URL = 'https://api.sunrise-sunset.org/json'


def get_sunrise_sunset(location: Location) -> tuple:
    print(f'Fetching sunrise and sunset times for {location.coordinate}')
    converter = MGRS()

    coords = converter.toLatLon(location.coordinate)

    params = {
        'date': 'today',
        'lat': coords[0],
        'lng': coords[1],
        'formatted': 0,
    }

    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()

    data = r.json()

    return data['results']['sunrise'][:-6]+'Z', data['results']['sunset'][:-6]+'Z'
