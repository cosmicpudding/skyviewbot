#!/usr/bin/env python
# ASTERICS-OBELICS Good Coding Practices (skyviewbot.py)
# V.A. Moss (vmoss.astro@gmail.com), with suggestions from T.J. Dijkema

__author__ = "YOUR NAME HERE"
__date__ = "$08-apr-2019 12:00:00$"
__version__ = "0.1"

import sys
from .functions import skyviewbot
from argparse import ArgumentParser, RawTextHelpFormatter


def main(*function_args):
    """Command-line interface to skyviewbot

    Args:
        List[str]: arguments (typically sys.argv[1:])

    Returns:
        bool: True if succeeded, False if not
    """

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('field', help="Field, e.g. 'M101'")
    parser.add_argument('msg', help="Message")
    parser.add_argument('-f', '--fits_name',
                        default=None,
                        type=str,
                        action="store",
                        help='Specify name of a custom fits file to use as input (default: %(default)s)')
    parser.add_argument('-i', '--slack_id',
                        default=None,
                        type=str,
                        help='Your slack ID')
    parser.add_argument('-s', '--survey',
                        default='DSS',
                        type=str,
                        help="Survey name, e.g. 'DSS' (default: %(default)s)")
    parser.add_argument('-r', '--radius',
                        default=1.,
                        type=float,
                        help="Radius (default: %(default)s")
    parser.add_argument('-c', '--colormap',
                        default="viridis",
                        type=str,
                        help="Colormap (default: %(default)s")
    parser.add_argument('-d', '--dry_run',
                        default=False,
                        action='store_true',
                        help='Dry run: make image, do not post to google and slack (default: %(default)s')
    args = parser.parse_args(*function_args)

    if not args.slack_id:
        print('You should use your Slack ID before posting!')
        return False

    return skyviewbot(args.slack_id, args.field, args.fits_name, args.msg, args.survey,
                      args.radius, args.colormap, dry_run=args.dry_run)


if __name__ == '__main__':
    main(sys.argv[1:])
