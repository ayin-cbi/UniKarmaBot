import os
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
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
