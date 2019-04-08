"""skyviewbot: a bot for posting skyview images to Slack

The main usage of skyviewbot is through the command-line interface skyviewbot.
The tool can be used with
>>> from skyviewbot import skyviewbot
"""

from .cli import main
from .functions import skyviewbot, call_skyview, coords_from_name, send_to_slack
