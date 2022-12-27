
import logging

from telegram.ext import CallbackContext
from telegram.botcommandscope import BotCommandScopeChat, BotCommandScopeAllGroupChats
from telegram import Update, BotCommand, constants

logger = logging.getLogger(__name__)


def command_start(update: Update, context: CallbackContext) -> None:
    logger.info(update.to_json())
    chat_id = update.message.chat['id']
    scope = BotCommandScopeChat(chat_id)
    list_commands = context.bot.get_my_commands(scope=scope)
    if len(list_commands):
        ask = BotCommand("ask", "ask")
        commands_chat = [ask]
        context.bot.set_my_commands(commands_chat, timeout=None, api_kwargs=None, scope=scope)

    logger.info("Commands was set")
