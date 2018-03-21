import global_vars
import parse
from datetime import datetime
from PIL import Image, ImageDraw
from global_vars import colors


class MyPainter:

    def __init__(self, image):
        self.draw = ImageDraw.Draw(image)
        self.draw.ellipse(
            (0, 0, image.size[0] - 1, image.size[1] - 1), outline='white')

    def drawStar(self, x, y, r, color):
        self.draw.ellipse((x - r, y - r, x + r, y + r),
                          fill=color, outline='black')

    def drawLabels(self, coords):
        for coord, label in zip(coords, global_vars.labels):
            self.draw.text((coord.x, coord.y), label)


def draw_image(sky, painter):
    for star in sky.get_stars():
        painter.drawStar(star.x, star.y, star.r, colors[star.color])
    if sky.in_pole():
        return
    painter.drawLabels(sky.get_labels())


def try_set_arguments(sky, coordinates, date_and_time):
    if date_and_time:
        sky.set_angle(parse.parse_time(date_and_time))

    if coordinates:
        sky.change_direction(
            *parse.parse_coordinates(
                coordinates[0].replace('_', '-'), coordinates[1]))


def make_screenshot(sky, name, coordinates, date_and_time):
    try_set_arguments(sky, coordinates, ' '.join(
        date_and_time))
    image = Image.new('RGB', (sky.height, sky.width))
    painter = MyPainter(image)
    draw_image(sky, painter)
    image.save(name)


def add_parser(subparsers):
    now = datetime.today().utcnow()
    parser_learn = subparsers.add_parser(
        'screenshot',
        help='Screenshot of the sky'
    )

    parser_learn.add_argument('name',
                              help='Name of the screen image\
                               (with the file extension)')
    parser_learn.add_argument('-c', '--coordinates',
                              default=('+90:00:00', '000:00:00'),
                              nargs=2,
                              help='''Coordinates of observer in spherical \
                              coordinate system in format d:m:s (where d is \
                              degree, m is minutes [0, 59], s is secunds \
                              [0, 59]). First argument is polar angle \
                              [_90, 90] (use symbol '_' instead of '-'), \
                              second is azimuthal angle [0, 360).''')
    parser_learn.add_argument('-d', '--datetime',
                              nargs=2,
                              default=('{}.{}.{}'.format(
                                  now.day, now.month, now.year),
                                  '{}:{}'.format(now.hour, now.minute)),
                              help='Date and time of \
                              observation in format d.m.Y H:M')
    parser_learn.set_defaults(func=lambda sky, options:
                              make_screenshot(sky, options.name,
                                              options.coordinates,
                                              options.datetime))
