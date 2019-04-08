#!/usr/bin/env python
# ASTERICS-OBELICS Good Coding Practices (skyviewbot.py)
# V.A. Moss (vmoss.astro@gmail.com), with suggestions from T.J. Dijkema

__author__ = "YOUR NAME HERE"
__date__ = "$08-apr-2019 12:00:00$"
__version__ = "0.1"

import os
import sys
from functions import *
from argparse import ArgumentParser, RawTextHelpFormatter
import aplpy
import matplotlib.pyplot as plt
import matplotlib as mpl

# Set matplotlib plotting parameters
# This is because the defaults are sub-optimal
# Maybe you can think of a better way to handle these parameters ;)
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True


def skyviewbot(*function_args):
    """Command-line interface to skyviewbot

    Args:
        List[str]: arguments (typically sys.argv[1:])

    Returns:
        bool: True if succeeded, False if not
    """

    # Make sure you use meaningful variable names!
    # Arguments should include:
    # - option to download from Skyview or use existing FITS file (included)
    # - survey to download from Skyview
    # - position to centre the field on
    # - field of view in degrees
    # - coordinate system for the image
    # - output image name to save as a JPEG
    # - colormap to use for imaging (optional!)
    # - option to include a colorbar or not (optional!)
    # - Slack ID of the user making the post
    # - custom colour to post to Slack (optional!)
    # - text to accompany the image posted to Slack (optional!)

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    # ARGUMENTS HERE!!
    parser.add_argument('field', help="Field, e.g. 'M101'")
    parser.add_argument('msg', help="Message")
    parser.add_argument('-s', '--skyview',
                        default=False,
                        action='store_true',
                        help='Specify whether to download a region from Skyview (default: %(default)s)')
    parser.add_argument('-d', '--dry_run',
                        default=False,
                        action='store_true',
                        help='Dry run: do download from skyview, do not post to google and slack (default: %(default)s')
    parser.add_argument('-f', '--fits_name',
                        default=None,
                        type=str,
                        help='Specify name of a custom fits file to use as input (default: %(default)s)')
    parser.add_argument('-i', '--slack_id',
                        default=None,
                        type=str,
                        help='Your slack ID')
    parser.add_argument('-n', '--survey',
                        default='DSS',
                        type=str,
                        help="Survey name, e.g. 'DSS' (default: %(default)s)")
    parser_args = parser.parse_args(*function_args)

    # Download an image of choice or use existing one

    # This section should be able to handle querying Skyview, using a custom FITS or the included one
    # Some possible ways to improve:
    # - maybe the region cutout has different width and height dimensions?
    # - maybe the user wants to select on wavelength type, e.g. radio, optical, etc
    # - what if the FITS file of choice is online somewhere, to be downloaded?
    # - what if the user can't get Java working, can you provide an astroquery.Skyview alternative?

    if not parser_args.slack_id:
        print('You should use your Slack ID before posting!')
        return False

    slack_id = parser_args.slack_id

    fieldname = parser_args.field
    ra, dec = coords_from_name(fieldname)

    if parser_args.skyview:
        # All parameters in this should be set properly using argparse
        # e.g. call_skyview(parser_args.field, parser_args.survey, parser_args.pos, parser_args.fov, parser_args.coord)
        fits_name = call_skyview(fieldname, parser_args.survey, (ra, dec), 1, 'J2000')
    elif parser_args.fits_name:
        fits_name = parser_args.fits_name
    else:
        print("Please specify either -s or -f")
        return False

    # Make an image using aplpy

    # Modify the below to be a function call in modules/functions.py
    # Make sure you include docstrings with your function to explain what it does!
    # Use the examples in functions.py to guide your docstring
    # With the following as options (add more if you want to):
    # - fits_name (file name of FITS image)
    # - colormap name
    # - optional to include a colorbar or not
    # - img_name (name of the produced output file)

    # Current parameters
    cmap_name = 'viridis'
    colorbar = True  # As an Aussie, I really struggle with American spelling in Python
    img_name = fits_name.replace(".fits", ".jpg")

    # Construct the figure
    f = aplpy.FITSFigure(fits_name, figsize=(10, 8))
    plt.title(fieldname)
    f.show_colorscale(cmap=cmap_name, stretch='linear')
    f.ticks.set_color('k')
    if colorbar:
        f.add_colorbar()

    # Note: bbox_inches='tight' gets rid of annoying white space, very useful!
    assert(os.path.isdir('results'))
    plt.savefig('results/' + img_name, dpi=200, bbox_inches='tight')

    # Upload the image to Google/Dropbox

    # This is done using a pre-written function included in modules/functions.py
    # Note: you need to login when prompted in the browser
    # With the autoskyview@gmail.com address, not your own!!!
    # See slides for login information
    # Possible way to improve:
    # - what if the user doesn't want to save everything to "results/"?
    # - what happens if something goes wrong with the image upload?

    img_path = 'results/' + img_name
    image_id = upload_to_google(img_path, dry_run=parser_args.dry_run)

    # Send the results to Slack

    # Modify the below to have these parameters set by your argparse arguments
    # Specifically (add more options if you want to):
    # - msg_color: colour of the message side
    # Note: if you add more options, you need to modify also send_to_slack()

    msg_color = '#3D99DD'  # Little known fact: this colour is known as Celestial Blue
    msg_text = parser_args.msg

    send_to_slack(msg_color, msg_text, fieldname, slack_id, image_id, dry_run=parser_args.dry_run)


if __name__ == '__main__':
    skyviewbot(sys.argv[1:])
