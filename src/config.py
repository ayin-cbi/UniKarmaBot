import os
import re
from dotenv import load_dotenv
from slackclient import SlackClient

load_dotenv()
# instantiate Slack client
BOT_ACCESS_TOKEN = os.environ.get('BOT_ACCESS_TOKEN')
if not BOT_ACCESS_TOKEN:
    raise Exception("No access token found! Can't connect to slack!")

SLACK_CLIENT = SlackClient(BOT_ACCESS_TOKEN)
# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
KARMA_TIMEOUT = 30
# Looks for <@user_id> +/- string
# Looks ahead to make sure, either message terminates or is followed by another karma group
# If not, does not parse as karma
KARMA_REGEX = re.compile(r"(?:^| )\<\@([\S]+)\> ?([\+\-]+)(?=[ ]*$|[ ]?(?=\<\@(?:[\S]+)\> ?([\+\-]+)))")

KARMA_URL = os.environ.get('KARMA_URL')

BUZZKILL = 100


# TODO: This is a channel ID for a
KARMABOT_ADMIN_CHANNEL = 'GDZ9KH17A'


KARMA_API_KEY = os.environ.get('KARMA_API_KEY')
if not KARMA_API_KEY:
    raise Exception("No API key found! Can't connect to the backend!")
