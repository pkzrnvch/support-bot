import argparse
import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intents(intents_training_dataset, project_id):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    for intent_title, intent_training_dataset in intents_training_dataset.items():
        training_phrases = []
        for question in intent_training_dataset['questions']:
            part = dialogflow.Intent.TrainingPhrase.Part(text=question)
            training_phrases.append(
                dialogflow.Intent.TrainingPhrase(parts=[part]))
        text = dialogflow.Intent.Message.Text(
            text=[intent_training_dataset['answer']])
        message = dialogflow.Intent.Message(text=text)
        intent = dialogflow.Intent(
            display_name=intent_title,
            training_phrases=training_phrases,
            messages=[message]
        )
        intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )


def main():
    load_dotenv()
    project_id = os.environ.get('PROJECT_ID')
    parser = argparse.ArgumentParser(description='DialogFlow training')
    parser.add_argument('filepath', help='JSON file with training dataset')
    args = parser.parse_args()
    with open(args.filepath, 'r') as training_file:
        intents_training_dataset = json.load(training_file)
    print(intents_training_dataset)
    create_intents(intents_training_dataset, project_id)


if __name__ == '__main__':
    main()
