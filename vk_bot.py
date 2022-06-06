import logging
import os

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from utils import get_dialogflow_reply


def vk_dialogflow_reply(event, vk_api):
    """DialogFLow reply to the user message."""
    reply_message = get_dialogflow_reply(
        event.user_id,
        event.text,
        fallbacks=False
    )
    if reply_message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply_message,
            random_id=get_random_id()
        )


def main():
    load_dotenv()
    vk_group_token = os.environ.get('VK_GROUP_TOKEN')
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            vk_dialogflow_reply(event, vk_api)


if __name__ == '__main__':
    main()
