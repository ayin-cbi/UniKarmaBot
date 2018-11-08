from config import SLACK_CLIENT

def post_message(channel, message):
    try:
        SLACK_CLIENT.rtm_send_message(channel, message)
    except Exception as e:
        logger.error('Exception')
        raise RuntimeError(e)
