from rest_framework.views import APIView
from permabots.serializers import UpdateSerializer
from permabots.models import TelegramBot, TelegramUser, TelegramChat, TelegramMessage, TelegramUpdate, TelegramCallbackQuery
from rest_framework.response import Response
from rest_framework import status
import logging
from permabots.tasks import handle_update
from datetime import datetime
from permabots import caching
import sys
import traceback


logger = logging.getLogger(__name__)

class OnlyTextMessages(Exception):
    pass


class TelegramHookView(APIView):    
    """
    View for Telegram webhook
    """
    
    def create_update(self, serializer, bot):
        if 'message' in serializer.data: 
            try:
                user = caching.get_or_set(TelegramUser, serializer.data['message']['from']['id'])
            except TelegramUser.DoesNotExist:
                user, _ = TelegramUser.objects.get_or_create(**serializer.data['message']['from'])
            try:
                chat = caching.get_or_set(TelegramChat, serializer.data['message']['chat']['id'])
            except TelegramChat.DoesNotExist:
                chat, _ = TelegramChat.objects.get_or_create(**serializer.data['message']['chat'])
            
            if 'text' not in serializer.data['message']:
                raise OnlyTextMessages
            message, _ = TelegramMessage.objects.get_or_create(message_id=serializer.data['message']['message_id'],
                                                               from_user=user,
                                                               date=datetime.fromtimestamp(serializer.data['message']['date']),
                                                               chat=chat,
                                                               text=serializer.data['message']['text'])
            update, _ = TelegramUpdate.objects.get_or_create(bot=bot,
                                                             update_id=serializer.data['update_id'],
                                                             message=message)
        
        elif 'callback_query' in serializer.data:
            # Message may be not present if it is very old
            if 'message' in serializer.data['callback_query']:
                try:
                    user = caching.get_or_set(TelegramUser, serializer.data['callback_query']['message']['from']['id'])
                except TelegramUser.DoesNotExist:
                    user, _ = TelegramUser.objects.get_or_create(**serializer.data['callback_query']['message']['from'])
                try:
                    chat = caching.get_or_set(TelegramChat, serializer.data['callback_query']['message']['chat']['id'])
                except TelegramChat.DoesNotExist:
                    chat, _ = TelegramChat.objects.get_or_create(**serializer.data['callback_query']['message']['chat'])
                
                message, _ = TelegramMessage.objects.get_or_create(message_id=serializer.data['callback_query']['message']['message_id'],
                                                                   from_user=user,
                                                                   date=datetime.fromtimestamp(serializer.data['callback_query']['message']['date']),
                                                                   chat=chat,
                                                                   text=serializer.data['callback_query']['message']['text'])
            else:
                message = None
            
            try:
                user = caching.get_or_set(TelegramUser, serializer.data['callback_query']['from']['id'])
            except TelegramUser.DoesNotExist:
                user, _ = TelegramUser.objects.get_or_create(**serializer.data['callback_query']['from'])
    
            callback_query, _ = TelegramCallbackQuery.objects.get_or_create(callback_id=serializer.data['callback_query']['id'],
                                                                            from_user=user,
                                                                            message=message,
                                                                            data=serializer.data['callback_query']['data'])
        
            update, _ = TelegramUpdate.objects.get_or_create(bot=bot,
                                                             update_id=serializer.data['update_id'],
                                                             callback_query=callback_query)            
        
        else:
            logger.error("Not valid message %s" % serializer.data)
            raise OnlyTextMessages
        caching.set(update)
        return update
    
    def post(self, request, hook_id):
        """
        Process Telegram webhook.
            1. Serialize Telegram message
            2. Get an enabled Telegram bot
            3. Create :class:`Update <permabots.models.telegram_api.Update>`
            5. Delay processing to a task      
            6. Response provider
        """
        serializer = UpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                bot = caching.get_or_set(TelegramBot, hook_id)
            except TelegramBot.DoesNotExist:
                logger.warning("Hook id %s not associated to an bot" % hook_id)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            try:
                update = self.create_update(serializer, bot)
                if bot.enabled:
                    logger.debug("Telegram Bot %s attending request %s" % (bot.token, request.data))
                    handle_update.delay(update.id, bot.id)
                else:
                    logger.error("Update %s ignored by disabled bot %s" % (update, bot.token))
            except OnlyTextMessages:
                logger.warning("Not text message %s for bot %s" % (request.data, hook_id))
                return Response(status=status.HTTP_200_OK)
            except:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)                
                logger.error("Error processing %s for bot %s" % (request.data, hook_id))
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error("Validation error: %s from message %s" % (serializer.errors, request.data))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)