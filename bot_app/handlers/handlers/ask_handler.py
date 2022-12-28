import openai
import logging
from telegram import Update
from telegram.ext import (CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters)
from botGPT.settings import MAX_TOKENS, MODEL, TEMPERATURE

logger = logging.getLogger(__name__)
QUESTION = range(1)


def ask(update: Update, context: CallbackContext):
    update.message.reply_text("ask me")
    return QUESTION


def get_question(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    prompt = update.message.text
    response = openai.Completion.create(model=MODEL, prompt=prompt, temperature=int(TEMPERATURE), max_tokens=int(MAX_TOKENS))
    logger.info(f"response {response}")
    for choice in response.choices:
        update.message.reply_text(f"response for {username}: {choice.text}")
    return ConversationHandler.END


def repeat_or_stop(update: Update, context: CallbackContext):
    _text_ = update.message['text']
    if str(_text_).lower() == 'stop':
        update.message.reply_text('Buy! See you later...')
        return ConversationHandler.END
    else:
        update.message.reply_text('You should reply on message. If you want to finished just type \"stop\"')


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Just try again...')
    return ConversationHandler.END


ask_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('ask', ask)],
    states={
        QUESTION: [MessageHandler(Filters.reply, get_question), MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)