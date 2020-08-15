#!/usr/bin/env pipenv-shebang

import subprocess
import yaml
from datetime import datetime
from sys import argv
from typing import List

from mission_profile import Mission
from report import Report


def read_mission_profile(profile: str) -> Mission:
    try:
        with open(profile) as file:
            raw = file.read()

        return yaml.safe_load(raw)

    except FileNotFoundError:
        print(f'Failed to find mission profile {profile}')
        exit(1)


def build_report_pdf(mission: Mission, sortie_reports: List[dict]):
    with open('wx-report.template', 'r') as file:
        template = file.read()

    report_files = ''
    for i, report in enumerate(sortie_reports):
        if i == 0:
            report_files += f'\\input{{{report["sortie"]}}}\n'
        else:
            report_files += f'\\include{{{report["sortie"]}}}\n'

        with open(f'{report["sortie"]}.md', 'w') as file:
            file.write(report['report'])

        subprocess.run(['pandoc', '-i', f'{report["sortie"]}.md', '-o', f'{report["sortie"]}.tex'])

    template = template.replace('%MISSION%', f'{mission.mission_name} ({mission.mission_number})')
    template = template.replace('%DATE%', f'{datetime.now().isoformat()[:-7]}Z')
    template = template.replace('%CONTENT%', report_files)

    with open('wx-report.tex', 'w') as file:
        file.write(template)

    subprocess.run(['pdflatex', '-halt-on-error', 'wx-report.tex'])
    subprocess.run(['pdflatex', '-halt-on-error', 'wx-report.tex'])


if __name__ == '__main__':
    if len(argv) < 2:
        print('Please provide a file to open')

    m = read_mission_profile(argv[1])

    if len(argv) > 2:
        r = Report(m, included_sorties=argv[2:])
    else:
        r = Report(m)

    s = []
    for i, sortie in enumerate(r.mission.sorties):
        if r.included_sorties and sortie.sortie_number not in r.included_sorties:
            continue
        s.append(r.get_sortie_report(i))

    build_report_pdf(m, s)
