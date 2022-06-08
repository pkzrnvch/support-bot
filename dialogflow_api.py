import os

from google.cloud import dialogflow


def get_dialogflow_reply(session_id, text):
    project_id = os.environ.get('PROJECT_ID')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    reply_message = response.query_result.fulfillment_text
    is_fallback = response.query_result.intent.is_fallback
    return reply_message, is_fallback
