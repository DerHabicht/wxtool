from adds import get_route_metars
from forecast import get_forecast_zone, get_forecast
from mission_profile import Mission
from usno import get_sunrise_sunset


class Report:
    mission = None
    included_sorties = None
    forecasts = {}

    def __init__(self, mission: Mission, included_sorties=None):
        self.mission = mission
        self.included_sorties = included_sorties

        if self.included_sorties:
            print(f'Generating report for sorties {", ".join(self.included_sorties)}')
        else:
            print('Generating report for all sorties.')

        for sortie in mission.sorties:
            if self.included_sorties and sortie.sortie_number not in self.included_sorties:
                print(f'Sortie {sortie.sortie_number} will not be included in the report.')
                continue

            sortie.route_wx = get_route_metars(sortie.route)

            for location in sortie.route:
                sunrise, sunset = get_sunrise_sunset(location)
                location.sunrise = sunrise
                location.sunset = sunset

                zone = get_forecast_zone(location)
                location.forecast_zone = zone[0]

                if zone not in self.forecasts:
                    self.forecasts[zone[0]] = {
                        'order': len(self.forecasts) + 1,
                        'name': zone[1],
                        'forecast': get_forecast(zone[0]),
                    }

    def get_sortie_report(self, idx: int) -> dict:
        sortie = self.mission.sorties[idx]
        collected_zones = set()
        report_lines = []
        waypoints = []

        for location in sortie.route:
            waypoints.append(f'| {location.name} | {location.coordinate} | {location.sunrise} | {location.sunset} |')

            if location.forecast_zone not in collected_zones:
                collected_zones.add(location.forecast_zone)
                report_lines.append(Report.assemble_forecast(self.forecasts[location.forecast_zone]))

        report = f'# Sortie {sortie.sortie_number} {{-}}\n\n'
        report += '## Route {-}\n\n| Location | Coordinate | Sunrise | Sunset |\n|--|--|--|--|\n'
        report += '\n'.join(waypoints) + '\n\n'
        report += f'## Recent Observations {{-}}\n{sortie.route_wx}\n\n'
        report += '## Area Forecasts {-}\n\n' + '\n'.join(report_lines)

        return {'sortie': sortie.sortie_number, 'report': report}

    @staticmethod
    def assemble_forecast(forecast: dict) -> str:
        report = f'### {forecast["name"]} {{-}}\n\n'

        for period in forecast['forecast']['periods']:
            report += f'#### {period["name"]} {{-}}\n{period["detailedForecast"]}\n\n'

        return report
