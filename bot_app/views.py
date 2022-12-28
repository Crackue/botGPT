import json
import logging

import openai
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from bot_app.handlers.onstart_handler import on_start_handler as on_start_menu_handler
from bot_app.handlers.handlers import ask_handler as ask_handler
from botGPT.settings import env
from telegram import Bot, Update
from telegram.ext import (Updater, CommandHandler, Dispatcher)
from botGPT.settings import DEBUG, BOT_TOKEN, WEB_HOOK_URL

logger = logging.getLogger(__name__)
DEBUG = env('DEBUG')
BOT_TOKEN = env('BOT_TOKEN')
TELEGRAM_URL = env('TELEGRAM_URL')
WEB_HOOK_URL = env('WEB_HOOK_URL')

n_workers = 1 if DEBUG else 4
bot = Bot(token=BOT_TOKEN)
_updater_ = Updater(token=BOT_TOKEN, workers=n_workers)


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", on_start_menu_handler.command_start))
    dp.add_handler(ask_handler.ask_conv_handler)
    return dp


def run_pooling(dispatcher: Dispatcher):
    setup_dispatcher(dispatcher)
    dispatcher.bot.delete_webhook()
    dispatcher.bot.set_webhook(f"{TELEGRAM_URL}{BOT_TOKEN}/setWebhook?url={WEB_HOOK_URL}/bot/webhook_post/")
    bot_info = dispatcher.bot.get_me()
    bot_link = f"https://t.me/{bot_info['username']}"
    logger.info(dispatcher.bot.getWebhookInfo())
    logger.info(f"Pooling of '{bot_link}' started")

    openai.api_key = env('OPENAIAPIKEY')


@csrf_exempt
def start_bot(request) -> HttpResponse:
    logger.info("START_BOT_REQUEST")
    run_pooling(_updater_.dispatcher)
    return HttpResponse("START_BOT_RESPONSE")


class TelegramBotWebhookView(View):
    @staticmethod
    def post(request, *args, **kwargs):
        process_telegram_event(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def get(request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})


def process_telegram_event(update_json):
    logger.info(update_json)
    update = Update.de_json(update_json, _updater_.bot)
    _updater_.dispatcher.process_update(update)


if bool(DEBUG):
    run_pooling(_updater_.dispatcher)
