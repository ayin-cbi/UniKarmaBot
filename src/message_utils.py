import random
from config import BUZZKILL

HAPPY_EMOJIS = [
    "unicorn_face",
    "grinning",
    "+1",
    "innocent",
    "money_mouth_face",
    "billy",
    "partyparrot",
    "gt",
    "bhangra",
    "bicep_left::tim::bicep_right", # Fuck off, I know
    "greenbuilding",
    "partytim",
    "carlton"
]

SAD_EMOJIS = [
    "scream",
    "skull_and_crossbones",
    "poop",
    "horse",
    "face_vomiting",
    "angry_unicorn",
    "badgt",
    "disapproval",
    "redbuilding"
]

BUZZKILL_EMOJIS = [
    "rotating_light",
    "oncoming_police_car",
    "radioactive_sign",
    "zap",
    "octagonal_sign",
    "wilted_flower",
    "alert",
    "10-4"
]


COMFORT_MESSAGES = [
    "Keep your chin up, kid.",
    "Someone out there loves you. Probably.",
    "You're #1 in my cold, unfeeling, robot heart.",
    "Smile! Billy the unicorn loves you!",
    "You are being comforted.",
    "Executing bin/comfort.sh",
    "Beep-boop is robot for 'I love you'",
    "There, there, don't be cry.",
    "Check this out buddy: https://www.reddit.com/r/aww"
]

COMFORT_EMOJIS = [
    "star2",
    "snowman",
    "rainbow",
    "unicorn_face",
    "billy",
    "tim",
    "rainbowcat"
]


CONFUSED_EMOJIS = [
    "shrug",
    "interrobang",
    "question"
]


def make_user_tag(user):
    return f"<@{user}>"


def make_emoji_tag(emoji):
    return f":{emoji}:"


def make_positive_message(giver, receiver, delta_receiver, total_receiver, karma_bot_id):
    message = f"{giver} has given {receiver} {delta_receiver} karma. "
    emoji = random.choice(HAPPY_EMOJIS)
    message += make_emoji_tag(emoji)
    message += f"\n{receiver} now has {total_receiver} karma."
    if receiver == make_user_tag(karma_bot_id):
        message += "\nThanks for the love! :heart_eyes:"
    return message

def make_negative_message(giver, receiver, delta_receiver, delta_giver, total_receiver, total_giver, karma_bot_id):
    message = f"{giver} has given {receiver} {delta_receiver} karma. "
    if receiver != giver:
        message += f"{giver} lost {abs(delta_giver)} karma. "
    emoji = random.choice(SAD_EMOJIS)
    message += make_emoji_tag(emoji)
    message += f"\n{receiver} now has {total_receiver} karma."

    if receiver != giver:
        message += f"{giver} now has {total_giver} karma."
    if receiver == make_user_tag(karma_bot_id):
        message += "\nI'm trying my best! :cry:"
    return message


def make_zero_message(giver, receiver):
    emoji = make_emoji_tag(random.choice(CONFUSED_EMOJIS))
    return f"{emoji} {giver} gave {receiver} NOTHING. {emoji}"


def make_buzzkill_message(message):
    buzzkill_emoji = make_emoji_tag(random.choice(BUZZKILL_EMOJIS))
    message += f"\n{buzzkill_emoji} BUZZKILL ENGAGED. MAXIMUM KARMA CHANGE IS {BUZZKILL} {buzzkill_emoji}"
    return message


def make_comfort_message():
    comfort_message = random.choice(COMFORT_MESSAGES)
    comfort_emoji = random.choice(COMFORT_EMOJIS)
    message = f":{comfort_emoji}: {comfort_message} :{comfort_emoji}:"
    return message
