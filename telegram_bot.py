import logging
import os

from dotenv import load_dotenv
from google.api_core import exceptions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils import get_dialogflow_reply, TelegramLogsHandler

logger = logging.getLogger(__name__)


def start(update, context):
    """Send greetings message when the command /start is issued."""
    update.message.reply_text('Добрый день! Какой у вас вопрос?')


def tg_dialogflow_reply(update, context):
    """DialogFLow reply to the user message."""
    try:
        update.message.reply_text(get_dialogflow_reply(
            update.effective_user.id,
            update.message.text))
    except exceptions.GoogleAPIError:
        logger.exception('GoogleAPIError')


def main():
    load_dotenv()
    tg_bot_token = os.environ.get('TG_BOT_TOKEN')
    tg_admin_id = os.environ.get('TG_LOGS_CHAT_ID')
    telegram_logs_handler = TelegramLogsHandler(tg_bot_token, tg_admin_id)
    telegram_logs_handler.setLevel(logging.WARNING)
    telegram_logs_handler.formatter = logging.Formatter(
        '%(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(
        handlers=[telegram_logs_handler]
    )
    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, tg_dialogflow_reply))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
