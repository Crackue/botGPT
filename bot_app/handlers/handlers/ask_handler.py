from telegram import Update
from telegram.ext import (CallbackContext, ConversationHandler)


def ask(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    if username:
        update.message.reply_text(f"response for {username}")
    else:
        update.message.reply_text("Oops! ask FAILED! :(")
    return ConversationHandler.END

