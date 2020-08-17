import yaml
from typing import List


class Mission(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Mission'

    mission_number = None
    mission_name = None
    sorties = None

    def __init__(self, mission_number: str, mission_name: str, sorties: List['Sortie']):
        self.mission_number = mission_number
        self.mission_name = mission_name
        self.sorties = sorties


class Sortie(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Sortie'

    sortie_number = None
    route = None
    route_metars = None
    route_tafs = None

    def __init__(self, sortie_number: str, route: List['Location']):
        self.sortie_number = sortie_number
        self.route = route


class Location(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Location'

    name = None
    coordinate = None
    forecast_zone = None
    sunrise = None
    sunset = None

    def __init__(self, name: str, coordinate: str):
        self.name = name
        self.coordinate = coordinate
