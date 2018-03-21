#!/usr/bin/python3
import argparse
import paint
import parse
import screenshot
from sys import argv
from stars import StarrySky
from geometry import Point


def init_parser():
    parser = argparse.ArgumentParser(prog="main")
    subparsers = parser.add_subparsers(
        title='available subcommands',
        description='',
        help='DESCRIPTION',
        metavar="SUBCOMMAND",
    )
    parser.add_argument('-W', '--width', type=int,
                        default=500, help='Width of the image')
    parser.add_argument('-H', '--height', type=int,
                        default=500, help='Height of the image')

    subparsers.required = True

    paint.add_parser(subparsers)
    screenshot.add_parser(subparsers)
    return parser


def main():
    parser = init_parser()
    parser = init_parser()
    options = parser.parse_args(argv[1:])

    sky = StarrySky(Point(0, 0, 1), Point(1, 0, 0), parse.read_stars(
    ), width=options.width, height=options.height)
    options.func(sky, options)

if __name__ == '__main__':
    main()
