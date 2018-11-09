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


def make_user_tag(user):
    return f"<@{user}>"


def make_emoji_tag(emoji):
    return f":{emoji}:"
