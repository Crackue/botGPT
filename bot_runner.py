import logging
import openai

from logging import config
import botGPT.settings
from bot_app.handlers.onstart_handler import on_start_handler as on_start_menu_handler
from bot_app.handlers.handlers import ask_handler as ask_handler
from botGPT.settings import env
from telegram.ext import (Updater, CommandHandler)
from botGPT.settings import DEBUG, BOT_TOKEN, WEB_HOOK_URL, TELEGRAM_URL

config.dictConfig(botGPT.settings.LOGGING)
logger = logging.getLogger(__name__)
n_workers = 1 if DEBUG else 4


class BotRunner:

    __slots__ = ('updater', 'token', 'num_workers')

    def __init__(self, token, num_workers):
        self.token = token
        self.num_workers = num_workers
        self.updater = Updater(token=self.token, workers=self.num_workers)

    def run_pooling(self):
        self.setup_dispatcher()
        self.updater.bot.delete_webhook()
        self.updater.bot.set_webhook(f"{TELEGRAM_URL}{BOT_TOKEN}/setWebhook?url={WEB_HOOK_URL}/bot/webhook_post/")
        logger.info(f"WebhookInfo {self.updater.bot.getWebhookInfo()}")
        logger.info(f"Pooling of '{self.updater.bot.get_me().link}' started")
        openai.api_key = env('OPENAIAPIKEY')
        return self

    def setup_dispatcher(self):
        self.updater.dispatcher.add_handler(CommandHandler("start", on_start_menu_handler.command_start))
        self.updater.dispatcher.add_handler(ask_handler.ask_conv_handler)
        return self.updater.dispatcher

    def get_updater(self):
        return self.updater


if __name__ == '__main__':
    BotRunner(token=BOT_TOKEN, num_workers=n_workers).run_pooling()
