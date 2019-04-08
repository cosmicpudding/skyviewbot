#!/usr/bin/env python
# ASTERICS-OBELICS Good Coding Practices (skyviewbot.py)
# V.A. Moss (vmoss.astro@gmail.com), with suggestions from T.J. Dijkema

__author__ = "YOUR NAME HERE"
__date__ = "$08-apr-2019 12:00:00$"
__version__ = "0.1"

import os
import sys
from .functions import *
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
    parser.add_argument('-d', '--dry_run',
                        default=False,
                        action='store_true',
                        help='Dry run: do download from skyview, do not post to google and slack (default: %(default)s')
    parser.add_argument('-f', '--fits_name',
                        default=None,
                        type=str,
                        action="store",
                        help='Specify name of a custom fits file to use as input (default: %(default)s)')
    parser.add_argument('-i', '--slack_id',
                        default=None,
                        type=str,
                        help='Your slack ID')
    parser.add_argument('-n', '--survey',
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
    parser_args = parser.parse_args(*function_args)

    if not parser_args.slack_id:
        print('You should use your Slack ID before posting!')
        return False

    slack_id = parser_args.slack_id

    fieldname = parser_args.field
    ra, dec = coords_from_name(fieldname)

    if parser_args.fits_name:
        fits_name = parser_args.fits_name
    else:
        fits_name = call_skyview(fieldname, parser_args.survey, (ra, dec), parser_args.radius, 'J2000')

    # Make an image using aplpy
    assert(os.path.isdir('results'))
    img_name = 'results/' + fits_name.replace(".fits", ".jpg")
    plot_fits(fits_name, fieldname, parser_args.colormap, True, img_name)

    # Upload the image to Google/Dropbox
    image_id = upload_to_google(img_name, dry_run=parser_args.dry_run)

    # Send the results to Slack
    msg_color = '#3D99DD'  # Little known fact: this colour is known as Celestial Blue
    msg_text = parser_args.msg
    send_to_slack(msg_color, msg_text, fieldname, slack_id, image_id, dry_run=parser_args.dry_run)


if __name__ == '__main__':
    main(sys.argv[1:])
