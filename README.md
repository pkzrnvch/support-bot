# User support bot

You can train this bot to answer users' standard questions. [DialogFlow](https://cloud.google.com/dialogflow) is used to recognize intents and provide responses.

Bot works with [Telegram](https://telegram.org/):

![](gifs/telegram_example.gif)

And [vk.com](https://vk.com/):

![](gifs/vk_example.gif)

## DialogFLow setup
You have to create:
- [Google cloud account and project](https://cloud.google.com/dialogflow/es/docs/quick/setup)
- [DialogFLow agent](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)
- [JSON key](https://cloud.google.com/docs/authentication/getting-started)

After creating a project you will get a project id, you will need it along with JSON key later.

## How to install
- Download project files and create virtual environment.
- Create an `.env` file in the project directory. Create a new telegram bot through a [BotFather](https://telegram.me/BotFather) and assign its token to `TG_BOT_TOKEN` variable.
- Send a message to [@UserInfoBot](https://t.me/userinfobot) to get your chat_id, assign it to `TG_LOGS_CHAT_ID` variable to receive log messages.
- Get your VK group API key from group's settings page and assign it to `VK_GROUP_API_KEY` variable.

Example of an `.env` file:
```
TG_BOT_TOKEN = 'Telegram bot token'
TG_LOGS_CHAT_ID = 'Telegram chat id to send log messages'
VK_GROUP_API_KEY = 'VK group api key'
GOOGLE_APPLICATION_CREDENTIALS = 'Path to the JSON key file'
PROJECT_ID = 'Google project id'
```

Python3 should already be installed. Use pip (or pip3, in case of conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```


## How to train bot
You need to create `JSON` file with intent titles, training phrases and responses with the following structure:
```json
{
    "How to apply for a job": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    "Forgot password or login": {
        "questions": [
            "Не помню пароль",
            "Не могу войти",
            "Проблемы со входом",
            "Забыл пароль",
            "Забыл логин",
            "Восстановить пароль",
            "Как восстановить пароль",
            "Неправильный логин или пароль",
            "Ошибка входа",
            "Не могу войти в аккаунт"
        ],
        "answer": "Если вы не можете войти на сайт, воспользуйтесь кнопкой «Забыли пароль?» под формой входа. Вам на почту прийдёт письмо с дальнейшими инструкциями. Проверьте папку «Спам», иногда письма попадают в неё."
    }}
```

To train the bot run the following command from the project directory:
```
python bot_training.py <path to the JSON file with training phrases>
```


### Usage

To run the bots locally use the following commands from the project directory:
```
python telegram_bot.py
```
```
python vk_bot.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [Devman](https://dvmn.org).