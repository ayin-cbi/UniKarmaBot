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
KARMA_TIMEOUT = 1
KARMA_REGEX = re.compile(r"(?:^| )\<\@([\S]+)\> ?([\+\-]+)")

KARMA_URL = os.environ.get('KARMA_URL')

BUZZKILL = 100


HAPPY_EMOJIS = [
    "unicorn_face",
    "grinning",
    "+1",
    "innocent",
    "money_mouth_face"
]

SAD_EMOJIS = [
    "scream",
    "skull_and_crossbones",
    "poop",
    "horse",
    "face_vomiting"
]

BUZZKILL_EMOJIS = [
    "rotating_light",
    "oncoming_police_car",
    "radioactive_sign",
    "zap",
    "octagonal_sign",
    "wilted_flower"
]


COMFORT_MESSAGES = [
    "Keep your chin up, kid.",
    "Someone out there loves you. Probably.",
    "You're #1 in my cold, unfeeling, robot heart.",
    "Smile! Billy the unicorn loves you!",
    "You are being comforted."
]

COMFORT_EMOJIS = [
    "full_moon_with_face",
    "sun_with_face",
    "star2",
    "snowman",
    "rainbow",
    "unicorn_face"
]
