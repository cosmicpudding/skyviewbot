#!/usr/bin/env python
# ASTERICS-OBELICS Good Coding Practices (skyviewbot.py)
# V.A. Moss (vmoss.astro@gmail.com), with suggestions from T.J. Dijkema

__author__ = "YOUR NAME HERE"
__date__ = "$08-apr-2019 12:00:00$"
__version__ = "0.1"

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


def skyviewbot(*args):
    """Command-line interface to skyviewbot"""

    # Make sure you use meaningful variable names!
    # Arguments should include:
    # - option to download from Skyview or use existing FITS file (included)
    # - custom field name
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
    parser.add_argument('-s', '--skyview',
                        default=False,
                        action='store_true',
                        help='Specify whether to download a region from Skyview (default: %(default)s)')
    parser.add_argument('-f', '--fits_name',
                        default=None,
                        type=str,
                        help='Specify name of a custom fits file to use as input (default: %(default)s)')
    parser_args = parser.parse_args(*args)

    # Download an image of choice or use existing one

    # This section should be able to handle querying Skyview, using a custom FITS or the included one
    # Some possible ways to improve:
    # - maybe the region cutout has different width and height dimensions?
    # - maybe the user wants to select on wavelength type, e.g. radio, optical, etc
    # - what if the FITS file of choice is online somewhere, to be downloaded?
    # - what if the user can't get Java working, can you provide an astroquery.Skyview alternative?

    if parser_args.skyview:
        # All parameters in this should be set properly using argparse
        # e.g. call_skyview(parser_args.field, parser_args.survey, parser_args.pos, parser_args.fov, parser_args.coord)
        fits_name = call_skyview('PKS1657-298', 'DSS', (255.291, -29.911), 1, 'J2000')
    elif parser_args.fits_name:
        fits_name = parser_args.fits_name
    else:
        fits_name = 'results/Skyview_PKS1657-298_DSS.fits'

    # This shouldn't be hardcoded, but set as an input argument in the parser above
    field = 'PKS1657-298'

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
    img_name = 'This_should_be_a_better_filename.jpg'

    # Construct the figure
    f = aplpy.FITSFigure(fits_name, figsize=(10, 8))
    plt.title(field)
    f.show_colorscale(cmap=cmap_name, stretch='linear')
    f.ticks.set_color('k')
    if colorbar:
        f.add_colorbar()

    # Note: bbox_inches='tight' gets rid of annoying white space, very useful!
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
    image_id = upload_to_google(img_path)

    # Send the results to Slack

    # Modify the below to have these parameters set by your argparse arguments
    # Specifically (add more options if you want to):
    # - msg_color: colour of the message side
    # - msg_text: text to accompany the post
    # - field: name of the field in your image
    # - slack_id: your Slack ID
    # Note: if you add more options, you need to modify also send_to_slack()

    msg_color = '#3D99DD'  # Little known fact: this colour is known as Celestial Blue
    msg_text = 'PKS1657-298 is a great galaxy, maybe the best galaxy.'  # 1707.01542
    slack_id = None  # This should be your own Slack ID, if you're testing the code

    # Check for Slack ID
    if not slack_id:
        send_to_slack(msg_color, msg_text, field, slack_id, image_id)
    else:
        print('You should change the ??? to be your Slack ID before posting! Exiting...')
        return


if __name__ == '__main__':
    skyviewbot(sys.argv[1:])
