import os
import logging

import telegram
from google.cloud import dialogflow


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=tg_bot_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_dialogflow_reply(session_id, text, fallbacks=True):
    project_id = os.environ.get('PROJECT_ID')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if not fallbacks and response.query_result.intent.is_fallback:
        return None
    return response.query_result.fulfillment_text
