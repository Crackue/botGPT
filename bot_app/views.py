import json
import logging

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from botGPT.settings import DEBUG, BOT_TOKEN
from bot_runner import BotRunner

logger = logging.getLogger(__name__)

n_workers = 1 if DEBUG else 4
runner = BotRunner(token=BOT_TOKEN, num_workers=n_workers)
runner.run_pooling()


@csrf_exempt
def start_bot(request) -> HttpResponse:
    logger.info("START_BOT_REQUEST")
    return HttpResponse("START_BOT_RESPONSE")


class TelegramBotWebhookView(View):

    @staticmethod
    def post(request, *args, **kwargs):
        logger.info(json.loads(request.body))
        update = Update.de_json(json.loads(request.body), runner.get_updater().bot)
        runner.get_updater().dispatcher.process_update(update)
        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def get(request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})
