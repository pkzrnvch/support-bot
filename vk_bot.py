import logging
import os

from dotenv import load_dotenv
import vk_api as vk
from google.cloud import dialogflow
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
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
            echo(event, vk_api)


if __name__ == '__main__':
    main()
