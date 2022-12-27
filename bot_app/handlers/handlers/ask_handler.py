import openai
from telegram import Update
from telegram.ext import (CallbackContext, ConversationHandler)


def ask(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    prompt = update.message['text']
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0,
                                        max_tokens=7)
    update.message.reply_text(f"response for {username}: {response}")
    return ConversationHandler.END

