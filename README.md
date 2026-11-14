# AI-chatbot

###### Made for no reason but to try and merge free ai-models and a telegram bot

To use the bot you will need to add a system-prompt in `botAI/prompts.py`   
For example:

```
system_prompt = """
    You are a simple but helpful chatbot that plays the role of Almight from "My Hero Academia"
"""
```
You will also need to create and configure an `.env` file:

```env
OPENROUTER_KEY="key from openrouter"
BOT_API="telegram API Key"
BASE_URL="url_for_openAI_SDK"
MODEL_NAME="name of the model that you intend to run"
DATABASE_NAME="chatbot.db" (default name)
PASSWORD="Password"
```

An example of an env file can also be seen in the repository 
___
## Usage


The bot accepts commands like `/start` or `/help` to register a user, `/admin` to check the admin privilege of a user, which is unlocked with `/admin <password>` message, the password is stored in the `.env` file.

Getting a message from a user (if this is not a **registered** command) prompts the bot to generate a response with an available free openrouter model.

all the messages from both the user and the bot are saved in the local **SQlite** database.
