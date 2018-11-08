import os
import time
import re
from slackclient import SlackClient

import requests
import json

from config import SLACK_CLIENT, RTM_READ_DELAY, KARMA_REGEX

# instantiate Slack client

# starterbot's user ID in Slack: value is assigned after the bot starts up
unikarmabot_id = None

def filter_and_parse(messages):
    karma_deltas = []
    for message in messages:
        # abort if it is not the right message type
        if message["type"] != "message":
            continue

        id_giver = message["user"]
        parsed_messages = parse_message(message["text"])
        karma_deltas += convert_to_karma_delta_dict(parsed_messages, id_giver)
    if karma_deltas:
        print(f"Karma_deltas {karma_deltas}")
    return karma_deltas


def parse_message(message_text):
    result = KARMA_REGEX.findall(message_text)
    return result


def convert_to_karma_delta_dict(parsed_messages, id_giver):
    messages = []
    for message in parsed_messages:
        temp = {
            "id_giver": id_giver,
            "id_recipient": message[0],
            "karma_delta": 0
        }
        counter = 0
        for char in message[1]:
            if char == "+":
                counter += 1
            elif char == "-":
                counter -= 1
        temp["karma_delta"] = counter
        messages.append(temp)
    return messages


def save_karma_deltas():
    pass


if __name__ == '__main__':
    print(SLACK_CLIENT)
    if SLACK_CLIENT.rtm_connect(with_team_state=False):
        print("Connected.")
        unikarmabot_id = SLACK_CLIENT.api_call("auth.test")["user_id"]
        print(unikarmabot_id)
        while True:
            messages = SLACK_CLIENT.rtm_read()
            karma_deltas = filter_and_parse(messages)
            save_karma_deltas(karma_deltas)
            # SLACK_CLIENT.rtm_send_message("CDX2XMKS6", "Hey Guys, I'm alive!")
            time.sleep(RTM_READ_DELAY)
