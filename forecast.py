import requests
from mgrs import MGRS

from mission_profile import Location


BASE_URL = 'https://api.weather.gov/zones'


def get_forecast_zone(location: Location) -> tuple:
    print(f'Fetching forcast zone for {location.coordinate}...')
    converter = MGRS()
    ll = converter.toLatLon(location.coordinate)

    params = {'type': 'forecast', 'point': f'{ll[0]},{ll[1]}'}
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    z = r.json()

    return z['features'][0]['properties']['id'], z['features'][0]['properties']['name']


def get_forecast(zone: str) -> dict:
    print(f'Fetching forecast for zone {zone}...')
    url = f'{BASE_URL}/forecast/{zone}/forecast'

    r = requests.get(url)
    r.raise_for_status()
    f = r.json()

    return f['properties']
