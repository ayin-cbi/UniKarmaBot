import os
import time
import re
import logging
from slackclient import SlackClient

import requests
import json
import random

from config import SLACK_CLIENT, RTM_READ_DELAY, KARMA_REGEX, KARMA_URL, KARMA_TIMEOUT, BUZZKILL, KARMABOT_ADMIN_CHANNEL, KARMA_API_KEY
from message_utils import (make_user_tag,
                           make_positive_message,
                           make_negative_message,
                           make_zero_message,
                           make_buzzkill_message,
                           make_comfort_message)
from math_utils import round_if_int

logging.basicConfig(level=logging.INFO)

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
        logging.debug(f"Karma_deltas {karma_deltas}")
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
            "karma": 0,
            "buzzkill": False
        }
        counter = 0
        for char in message[1][1:]:
            if char == "+":
                counter += 1
            elif char == "-":
                counter -= 1

        if abs(counter) > BUZZKILL:
            karma_delta_dict["buzzkill"] = True
        karma_delta_dict["karma"] = max(min(counter, BUZZKILL), -1*BUZZKILL)

        if id_giver == message[0]:
            if counter < 0:
                message = make_comfort_message()
                SLACK_CLIENT.rtm_send_message(id_channel, message)
                continue
            if counter > 0:
                karma_delta_dict["karma"] = -1*karma_delta_dict["karma"]

        messages.append(karma_delta_dict)
    return messages


def save_karma_deltas(karma_deltas):
    karma_responses = []
    if not KARMA_URL:
        raise RuntimeError("No Karma URL provided")
    for karma in karma_deltas:

        request_data = {"karma": karma}
        try:
            r = requests.post(KARMA_URL, headers= {'Authorization': KARMA_API_KEY}, json=request_data, timeout=KARMA_TIMEOUT)
            if r.status_code != 200:
                raise requests.exceptions.ConnectionError(f"Error reaching Karma backend: {r.status_code}, {r.text}")
            r_json = r.json()
            r_json["slack_id_channel"] = karma["slack_id_channel"]
            r_json["buzzkill"] = karma["buzzkill"]
            logging.info(f"GOT status code: {r.status_code}")
            logging.info(f"GOT text: {r_json}")
            karma_responses.append(r_json)
        except requests.exceptions.Timeout:
            message = "Karma request timed out. Try again when I'm not so tired."
            SLACK_CLIENT.rtm_send_message(karma["slack_id_channel"], message)
    return karma_responses


def send_karma_responses(karma_responses):
    for karma_response in karma_responses:
        channel = karma_response["slack_id_channel"]
        id_giver = karma_response["id_giver"]
        id_receiver = karma_response["id_receiver"]
        delta_giver = round_if_int(karma_response["delta_giver"])
        delta_receiver = round_if_int(karma_response["delta_receiver"])
        total_giver = karma_response["total_giver"]
        total_receiver = karma_response["total_receiver"]

        giver = make_user_tag(id_giver)
        receiver = make_user_tag(id_receiver)

        if delta_receiver > 0:
            message = make_positive_message(giver, receiver, delta_receiver, total_receiver)
        elif delta_receiver < 0:
            message = make_negative_message(giver, receiver, delta_receiver, delta_giver, total_receiver, total_giver)
        else:
            message = make_zero_message(giver, receiver)
        if karma_response["buzzkill"]:
            message = make_buzzkill_message(message)
        SLACK_CLIENT.rtm_send_message(channel, message)


if __name__ == '__main__':
    if SLACK_CLIENT.rtm_connect(with_team_state=False):
        logging.info("Connected to Slack.")
        unikarmabot_id = SLACK_CLIENT.api_call("auth.test")["user_id"]
        while True:
            try:
                messages = SLACK_CLIENT.rtm_read()
                karma_deltas = filter_and_parse(messages)
                karma_responses = save_karma_deltas(karma_deltas)
                if karma_responses:
                    send_karma_responses(karma_responses)
                time.sleep(RTM_READ_DELAY)

            except KeyboardInterrupt:
                logging.info("Shutting down the bot.")
                break
            except Exception as e:
                logging.error(f"Oof ouch something bad happened:\n{e}")
                try:
                    if KARMABOT_ADMIN_CHANNEL:
                        message = f"<!here> Something went wrong:\n{e}"
                        SLACK_CLIENT.rtm_send_message(KARMABOT_ADMIN_CHANNEL, message)
                except Exception as e:
                    logging.error(f"I'm trying to talk but you won't listen!\n{e}")

