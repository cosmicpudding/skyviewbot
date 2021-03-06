#!/usr/bin/env python
"""Command-line interface for skyviewbot"""

# ASTERICS-OBELICS Good Coding Practices (skyviewbot.py)
# V.A. Moss (vmoss.astro@gmail.com), with suggestions from T.J. Dijkema

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
    parser.add_argument('field', help='Field, e.g. "M101" or "255.2,1" (if it contains a comma, '
                                      'it\'s interpreted as coordinates, otherwise fed to CDS)')
    parser.add_argument('msg', help="Message to accompany the post on Slack")
    parser.add_argument('-f', '--fits-name',
                        default=None,
                        type=str,
                        action="store",
                        help='Specify name of a custom fits file to use as input instead of Skyview (default: %(default)s)')
    parser.add_argument('-i', '--slack-id',
                        default=None,
                        type=str,
                        help='Your Slack ID (default: %(default)s)')
    parser.add_argument('-s', '--survey',
                        default='DSS',
                        type=str,
                        help="Survey name, e.g. 'DSS' (default: %(default)s)")
    parser.add_argument('-r', '--radius',
                        default=1.,
                        type=float,
                        help="Radius (default: %(default)s)")
    parser.add_argument('-c', '--colormap',
                        default="viridis",
                        type=str,
                        help="Colormap (default: %(default)s)")
    parser.add_argument('-d', '--dry-run',
                        default=False,
                        action='store_true',
                        help='Dry run: make image, do not post to google and slack (default: %(default)s')
    args = parser.parse_args(*function_args)

    if not args.slack_id:
        print('You should use your Slack ID before posting!')
        return False

    retval = skyviewbot(args.slack_id, args.field, args.fits_name, args.msg, args.survey,
                        args.radius, args.colormap, dry_run=args.dry_run)

    if retval:
        print("SkyViewBot posted to Slack successfully")
    else:
        print("Some error happened in SkyViewBot")

    return retval


if __name__ == '__main__':
    main(sys.argv[1:])
