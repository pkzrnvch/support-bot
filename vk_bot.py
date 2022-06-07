import logging
import os

import requests
import vk_api as vk
from dotenv import load_dotenv
from google.api_core import exceptions
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from utils import get_dialogflow_reply, TelegramLogsHandler


logger = logging.getLogger(__name__)


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
    tg_bot_token = os.environ.get('TG_BOT_TOKEN')
    tg_admin_id = os.environ.get('TG_LOGS_CHAT_ID')
    telegram_logs_handler = TelegramLogsHandler(tg_bot_token, tg_admin_id)
    telegram_logs_handler.setLevel(logging.WARNING)
    telegram_logs_handler.formatter = logging.Formatter(
        '%(name)s - %(levelname)s - %(msg)s')
    logger.addHandler(telegram_logs_handler)
    try:
        vk_session = vk.VkApi(token=vk_group_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                vk_dialogflow_reply(event, vk_api)
    except exceptions.GoogleAPIError:
        logger.exception('GoogleAPIError')
    except vk.exceptions.VkApiError:
        logger.exception('VkApiError')
    except requests.exceptions.RequestException:
        logger.exception('RequestsException')


if __name__ == '__main__':
    main()
