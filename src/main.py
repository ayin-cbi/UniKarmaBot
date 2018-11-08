import os
import time
import re
import logging
from slackclient import SlackClient

import requests
import json

from config import SLACK_CLIENT, RTM_READ_DELAY, KARMA_REGEX, KARMA_URL

# instantiate Slack client

# starterbot's user ID in Slack: value is assigned after the bot starts up
unikarmabot_id = None

def filter_and_parse(messages):
    karma_deltas = []
    for message in messages:
        # abort if it is not the right message type
        if "type" not in message.keys() or message["type"] != "message":
            continue
        try:
            id_giver = message["user"]
            id_channel = message["channel"]
            parsed_messages = parse_message(message["text"])
            karma_deltas += convert_to_karma_delta_dict(parsed_messages, id_giver, id_channel)
        except Exception as e:
            logging.warn(f"Exception thrown in filter_and_parse: {e}")
    if karma_deltas:
        print(f"Karma_deltas {karma_deltas}")
    return karma_deltas


def parse_message(message_text):
    result = KARMA_REGEX.findall(message_text)
    return result


def convert_to_karma_delta_dict(parsed_messages, id_giver, id_channel):
    messages = []
    for message in parsed_messages:
        karma_delta_dict = {
            "slack_id_channel": id_channel,
            "slack_id_giver": id_giver,
            "slack_id_receiver": message[0],
            "karma": 0
        }
        counter = 0
        for char in message[1]:
            if char == "+":
                counter += 1
            elif char == "-":
                counter -= 1
        karma_delta_dict["karma"] = counter
        messages.append(karma_delta_dict)
    return messages


def save_karma_deltas(karma_deltas):
    if not KARMA_URL:
        raise RuntimeError("No Karma URL provided")
    for karma in karma_deltas:
        print(f"ATTEMPTING POST TO: {KARMA_URL}")
        print(f"ATTEMPTING POST: {karma}")
        request_data = {
            "karma": karma
        }
        # print(f"{json.dumps(request_data)}")
        r = requests.post(KARMA_URL, json=request_data)
        print(f"GOT status code: {r.status_code}")
        print(f"GOT text: {r.json()}")


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
            for karma_delta in karma_deltas:
                channel = karma_delta["slack_id_channel"]
                id_giver = karma_delta["slack_id_giver"]
                id_receiver = karma_delta["slack_id_receiver"]
                karma = karma_delta["karma"]
                message = f"<@{id_giver}> has given <@{id_receiver}> {karma} karma.  <@{id_receiver}> now has TOTAL karma"
                SLACK_CLIENT.rtm_send_message(channel, message)
            time.sleep(RTM_READ_DELAY)
