import os
import re
import sys
from datetime import datetime
from geometry import spherical_to_decart
from stars import Star
from collections import defaultdict


minimum_date = datetime.strptime('1.1.2000 00:00', '%d.%m.%Y %H:%M')
maximum_date = datetime.strptime('31.12.2099 23:59', '%d.%m.%Y %H:%M')
r = re.compile(r'(-?\+?\d+):(\d+):(\d+)')


GREEK = defaultdict(lambda: None, {
    'Alp': u'\u03B1',
    'Bet': u'\u03B2',
    'Gam': u'\u03B3',
    'Del': u'\u03B4',
    'Eps': u'\u03B5',
    'Zet': u'\u03B6',
    'Eta': u'\u03B7',
    'The': u'\u03B8',
    'Iot': u'\u03B9',
    'Kap': u'\u03BA',
    'Lam': u'\u03BB',
    'Mu ': u'\u03BC',
    'Nu ': u'\u03BD',
    'Xi ': u'\u03BE',
    'Omi': u'\u03BF',
    'Pi ': u'\u03C0',
    'Rho': u'\u03C1',
    'Sig': u'\u03C3',
    'Tau': u'\u03C4',
    'Ips': u'\u03C5',
    'Phi': u'\u03C6',
    'Chi': u'\u03C7',
    'Psi': u'\u03C8',
    'Ome': u'\u03C9',
})


def convert_hours_to_angle(s):
    l = list(map(int, re.split(r'[^\d+-]', s)))
    return (l[0] + (l[1] + (l[2] + l[3] / 10) / 60) / 60) * 15


def convert_str_to_angle(s):
    l = list(map(int, filter(lambda x: len(x) > 0, re.split(r'[^\d+-]', s))))
    if l[1] >= 60 or l[2] >= 60:
        return None
    return l[0] + (l[1] + l[2] / 60) / 60


def parse_line(line, name):
    alpha = convert_hours_to_angle(line[4:14].replace(' ', '0'))
    delta = convert_str_to_angle(line[16:24].replace(' ', '0'))
    if line[15] == '-':
        delta = -delta
    delta = 90 - delta
    color = line[49]
    let = line[103:106]
    m = float(line[41:46].replace(' ', '0'))
    return Star(spherical_to_decart(alpha, delta), color, m, name, GREEK[let])


def read_stars():
    st = []
    directory = 'txt/'
    files = os.listdir(directory)
    for file in files:
        name = os.path.splitext(file)[0]
        with open(directory + file) as f:
            for l in f.readlines():
                st.append(parse_line(l, name))
    return st


def check_angle(angle, max_value, min_value=0):
    return angle[0] <= max_value and angle[1] < 60 and angle[2] < 60


def parse_time(time):
    try:
        time = datetime.strptime(time, '%d.%m.%Y %H:%M')
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    if not (minimum_date <= time <= maximum_date):
        print(
            'Choose datetime in range \
[1.1.2000 00:00, 31.12.2099 23:59]\
', file=sys.stderr)
        sys.exit(1)
    return int((time - minimum_date).total_seconds()) * 1000


def parse_coordinates(phi, theta):
    if not (r.fullmatch(phi) and r.fullmatch(theta)):
        print('Write coordinates in a correct format', file=sys.stderr)
        sys.exit(1)

    if not (-90 <= convert_str_to_angle(phi) <= 90 and
            0 <= convert_str_to_angle(theta) <= 360):
        print('Write coordinates in a correct range', file=sys.stderr)
        sys.exit(1)

    return phi, theta
