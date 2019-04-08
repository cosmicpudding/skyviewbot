#!/usr/bin/env python
# ASTERICS-OBELICS Good Coding Practices (functions.py)
# V.A. Moss (vmoss.astro@gmail.com), with suggestions from T.J. Dijkema

__author__ = "YOUR NAME HERE"
__date__ = "$08-apr-2019 12:00:00$"
__version__ = "0.1"

import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from astroquery.skyview import SkyView
from astropy.coordinates import SkyCoord
import astropy.units as u


def call_skyview(field, survey, pos, fov, coord, proj='Car', pix=500):
    """Call Skyview to download data from a survey based on input parameters

    Args:
        field (str): name of the field, used in naming the output file
        survey (str): name of survey, from https://skyview.gsfc.nasa.gov/current/cgi/survey.pl
        pos (float,float): position coordinates as a tuple
        fov (float): FOV in degrees
        coord (str): coordinate system (e.g. Galactic, J2000, B1950)
        proj (str): projection of image. (e.g. Car, Sin)
        pix (int): pixel dimensions of image (e.g. 500)

    Returns:
        str: name of resulting fits file

    Examples:
        >>> call_skyview('pks1657-298', 'dss', (255.291,-29.911), 5, 'J2000')
        'skyview_pks1657-298_dss.fits'
        >>> call_skyview('B0329+54', 'nvss', (144.99497,-01.22029), 0.5, 'Gal')
        'skyview_B0329+54_nvss.fits'
    """

    x, y = pos

    images = SkyView.get_images(SkyCoord(ra=x*u.deg, dec=y*u.deg), survey,
                                coordinates=coord,
                                projection=proj, pixels=pix,
                                height=fov*u.deg, width=fov*u.deg)

    # Construct name of the resulting file
    fitsname = "Skyview_{field}_{survey}.fits".format(**locals())

    images[0][0].writeto(fitsname)

    return (fitsname)


def upload_to_google(img_path):
    """Upload a file using Google API to Google Drive folder

    Args:
        filename (str): name of file to upload, including path

    Returns:
        image_id (str): Google Drive image ID

    Examples:
        >>> upload_to_google("test.jpg")
    """

    # Upload the resulting image to Google Drive
    # This connects to a specific account made for this exercise

    # This is a shared folder so automatically gives uploaded files read/write permission
    folder_id = "1OuvohOT1aBpYBLToG5eIJbfdW-Z5a8Nj"

    # Set up authorisation
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    with open(img_path, "r") as img_file:
        pass
        #file_drive = drive.CreateFile({'title': os.path.basename(img_file.name), "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
        #file_drive.SetContentFile(img_path)
        #file_drive.Upload()

    # This part returns the Google Drive ID of the file
    # We need this for the Slack upload
    return file_drive['id']


def send_to_slack(msg_color, msg_text, field, slack_id, image_id):
    """Send a post to Slack using Slack webhooks

    Args:
        msg_color (str): any of 'good','warning', 'danger' or a HEX color
        msg_text (str): text of choice to accompany the post
        field (str): name of the field shown in the image posted
        slack_id (str): poster's Slack ID e.g. 'UH0H2QFC2'
        image_id (str): id of chosen image from Google Drive upload

    Returns:
        None

    Examples:
        >>> send_to_slack('#3A143E', 'Test', 'Test', 'UH0H2QFC2', '1qWyC6xAHODREDfoZLH4qTYTDwt5m3EEk')
    """

    # Replace characters in message text
    msg_text = msg_text.replace("'", "")

    # Construct the full message
    full_msg = """{
    "attachments": [
        {
            "color": "%s",
            "author_name": "<@%s>",
            "title": "SkyviewBot Image Post: %s",
            "text": "%s",
            "image_url" : "http://drive.google.com/uc?export=download&id=%s"
       }
    ]
}""" % (msg_color, slack_id, field, msg_text, image_id)

    # Send the command
    cmd = """curl -X POST --data-urlencode 'payload=%s' https://hooks.slack.com/services/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""" % (full_msg)
    print(cmd)
    #os.system(cmd)
