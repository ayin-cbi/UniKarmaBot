import os
import time
import re
from slackclient import SlackClient

from config import SLACK_CLIENT, RTM_READ_DELAY

# instantiate Slack client

# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None


if __name__ == '__main__':
    print(SLACK_CLIENT)
    if SLACK_CLIENT.rtm_connect(with_team_state=False):
        print("Connected.")
        starterbot_id = SLACK_CLIENT.api_call("auth.test")["user_id"]
        print(starterbot_id)
        while True:
            print(SLACK_CLIENT.rtm_read())
            # SLACK_CLIENT.rtm_send_message("CDX2XMKS6", "Hey Guys, I'm alive!")
            time.sleep(RTM_READ_DELAY)
