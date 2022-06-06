import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils import get_dialogflow_reply


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send greetings message when the command /start is issued."""
    update.message.reply_text('Добрый день! Какой у вас вопрос?')


def tg_dialogflow_reply(update, context):
    """DialogFLow reply to the user message."""
    update.message.reply_text(get_dialogflow_reply(
        update.effective_user.id,
        update.message.text))


def main():
    load_dotenv()
    tg_bot_token = os.environ.get('TG_BOT_TOKEN')
    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, tg_dialogflow_reply))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
