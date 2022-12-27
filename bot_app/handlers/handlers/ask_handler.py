import openai
import logging
from telegram import Update
from telegram.ext import (CallbackContext, ConversationHandler)


logger = logging.getLogger(__name__)


def ask(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    prompt = update.message['text']
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=7)
    for choice in response.choices:
        logger.info(f"response {response.choices[0].text}")
        update.message.reply_text(f"response for {username}:\nchoice {choice.index}: {choice.text}")
    return ConversationHandler.END
