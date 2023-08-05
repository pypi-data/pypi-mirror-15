# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from telegram import Bot as TelegramBotAPI
from kik import KikApi
import logging
from microbot.models.base import MicrobotModel
from microbot.models import TelegramUser, TelegramChatState, KikChatState
from django.core.urlresolvers import RegexURLResolver
from django.core.urlresolvers import Resolver404
from telegram import ParseMode, ReplyKeyboardHide, ReplyKeyboardMarkup
from telegram.bot import InvalidToken
import ast
from django.conf import settings
from django.db.models import Q
from microbot import validators
from kik.messages.responses import TextResponse
from kik.messages.text import TextMessage
from kik.messages.keyboards import SuggestedResponseKeyboard
from kik.configuration import Configuration
import sys

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Bot(MicrobotModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bots', help_text=_("User who owns the bot"))
    name = models.CharField(_('Name'), max_length=100, db_index=True, help_text=_("Name for the bot"))
    telegram_bot = models.OneToOneField('TelegramBot', verbose_name=_("Telegram Bot"), related_name='bot', 
                                        on_delete=models.SET_NULL, blank=True, null=True,
                                        help_text=_("Telegram Bot"))
    
    kik_bot = models.OneToOneField('KikBot', verbose_name=_("Kik Bot"), related_name='bot',
                                   on_delete=models.SET_NULL, blank=True, null=True,
                                   help_text=_("Kik Bot"))
    
    class Meta:
        verbose_name = _('Bot')
        verbose_name_plural = _('Bots')    
        
    def __str__(self):
        return '%s' % self.name
    
    def update_chat_state(self, bot_service, message, chat_state, target_state, context):
        context_target_state = chat_state.state.name.lower().replace(" ", "_") if chat_state else '_start'
        if not chat_state:
                logger.warning("Chat state for update chat %s not exists" % 
                               (message.chat.id))
                bot_service.create_chat_state(message, target_state, {context_target_state: context})
        else:
            if chat_state.state != target_state:                
                state_context = chat_state.ctx
                state_context[context_target_state] = context
                chat_state.ctx = state_context
                chat_state.state = target_state
                chat_state.save()
                logger.debug("Chat state updated:%s for message %s with (%s,%s)" % 
                             (target_state, message, chat_state.state, context))
            else:
                logger.debug("ChateState stays in %s" % target_state)
    
    def handle_message(self, message, bot_service):
        urlpatterns = []
        state_context = {}
        chat_state = bot_service.get_chat_state(message)
        if chat_state:
            state_context = chat_state.ctx
            for handler in self.handlers.select_related('response', 'request').filter(Q(enabled=True), 
                                                                                      Q(source_states=chat_state.state) | Q(source_states=None)):
                urlpatterns.append(handler.urlpattern())
        else:
            for handler in self.handlers.select_related('response', 'request').filter(enabled=True, source_states=None):
                urlpatterns.append(handler.urlpattern())
        
        resolver = RegexURLResolver(r'^', urlpatterns)
        try:
            resolver_match = resolver.resolve(bot_service.message_text(message))
        except Resolver404:
            logger.warning("Handler not found for %s" % message)
        else:
            callback, callback_args, callback_kwargs = resolver_match
            logger.debug("Calling callback:%s for message %s with %s" % 
                         (callback, message, callback_kwargs))
            text, keyboard, target_state, context = callback(self, message=message, service=bot_service.identity, 
                                                             state_context=state_context, **callback_kwargs)
            if target_state:
                self.update_chat_state(bot_service, message, chat_state, target_state, context)
            keyboard = bot_service.build_keyboard(keyboard)
            bot_service.send_message(bot_service.get_chat_id(message), text, keyboard, message)
            
    def handle_hook(self, hook, data):
        logger.debug("Calling hook %s process: with %s" % (hook.key, data))
        text, keyboard = hook.process(self, data)
        if hook.bot.telegram_bot and hook.bot.telegram_bot.enabled:
            telegram_keyboard = hook.bot.telegram_bot.build_keyboard(keyboard)
            for recipient in hook.telegram_recipients.all():
                hook.bot.telegram_bot.send_message(recipient.chat_id, text, telegram_keyboard)
        if hook.bot.kik_bot and hook.bot.kik_bot.enabled:
            kik_keyboard = hook.bot.kik_bot.build_keyboard(keyboard)
            for recipient in hook.kik_recipients.all():
                hook.bot.kik_bot.send_message(recipient.chat_id, text, kik_keyboard, user=recipient.username)
            
class IntegrationBot(MicrobotModel): 
    enabled = models.BooleanField(_('Enable'), default=True, help_text=_("Enable/disable telegram bot"))

    class Meta:
        verbose_name = _('Integration Bot')
        verbose_name_plural = _('Integration Bots')
        abstract = True
        
    def init_bot(self):
        raise NotImplementedError
    
    def set_webhook(self, url):
        raise NotImplementedError
    
    @property
    def hook_url(self):
        raise NotImplementedError
        
    @property
    def hook_id(self):
        raise NotImplementedError
    
    @property
    def identity(self):
        raise NotImplemented
    
    @property
    def null_url(self):
        raise NotImplementedError
    
    def message_text(self, message):
        raise NotImplementedError
    
    def get_chat_state(self, message):
        raise NotImplementedError
        
    def build_keyboard(self, keyboard):       
        raise NotImplementedError
        
    def send_message(self, chat_id, text, keyboard, reply_message=None, user=None):
        raise NotImplementedError
    
    def create_chat_state(self, message, target_state, context):
        raise NotImplementedError
    
    def batch(self, iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx+n, l)], ndx+n >= l
    
@python_2_unicode_compatible
class TelegramBot(IntegrationBot):    
    token = models.CharField(_('Token'), max_length=100, db_index=True, unique=True, validators=[validators.validate_token],
                             help_text=_("Token provided by Telegram API https://core.telegram.org/bots"))
    user_api = models.OneToOneField(TelegramUser, verbose_name=_("Telegram Bot User"), related_name='telegram_bot', 
                                    on_delete=models.CASCADE, blank=True, null=True,
                                    help_text=_("Telegram API info. Automatically retrieved from Telegram"))
    
    class Meta:
        verbose_name = _('Telegram Bot')
        verbose_name_plural = _('Telegram Bots')    
    
    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__(*args, **kwargs)
        self._bot = None
        if self.token:
            try:
                self.init_bot()
            except InvalidToken:
                logger.warning("Incorrect token %s" % self.token)
            
    def __str__(self):
        return "%s" % (self.user_api.first_name or self.token if self.user_api else self.token)
    
    def init_bot(self):
        self._bot = TelegramBotAPI(self.token)
    
    @property
    def hook_id(self):
        return str(self.id)
    
    @property
    def hook_url(self):
        return 'microbot:telegrambot'
    
    @property
    def null_url(self):
        return None
    
    @property
    def identity(self):
        return 'telegram'
    
    def set_webhook(self, url):
        self._bot.setWebhook(webhook_url=url)
    
    def message_text(self, message):
        return message.text
    
    def get_chat_state(self, message):
        try:
            return TelegramChatState.objects.get(chat=message.chat, user=message.from_user, state__bot=self.bot)
        except TelegramChatState.DoesNotExist:
            return None
        
    def build_keyboard(self, keyboard):       
        if keyboard:
            keyboard = ast.literal_eval(keyboard)
            keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        else:
            keyboard = ReplyKeyboardHide()
        return keyboard
        
    def create_chat_state(self, message, target_state, context):
        TelegramChatState.objects.create(chat=message.chat,
                                         user=message.from_user,
                                         state=target_state,
                                         ctx=context)
              
    def get_chat_id(self, message):
        return message.chat.id
    
    def send_message(self, chat_id, text, keyboard, reply_message=None, user=None):
        parse_mode = ParseMode.HTML
        disable_web_page_preview = True
        reply_to_message_id = None
        if reply_message:
            reply_to_message_id = reply_message.message_id
        for chunk_text, last in self.batch(text, 4096):
            try:
                keyboard_to_send = None
                if last:
                    keyboard_to_send = keyboard
                logger.debug("Message to send:(chat:%s,text:%s,parse_mode:%s,disable_preview:%s,keyboard:%s, reply_to_message_id:%s" %
                             (chat_id, chunk_text, parse_mode, disable_web_page_preview, keyboard_to_send, reply_to_message_id))
                self._bot.sendMessage(chat_id=chat_id, text=chunk_text, parse_mode=parse_mode, 
                                      disable_web_page_preview=disable_web_page_preview, reply_markup=keyboard_to_send, 
                                      reply_to_message_id=reply_to_message_id)        
                logger.debug("Message sent OK:(chat:%s,text:%s,parse_mode:%s,disable_preview:%s,reply_keyboard:%s, reply_to_message_id:%s" %
                             (chat_id, chunk_text, parse_mode, disable_web_page_preview, keyboard_to_send, reply_to_message_id))
            except:
                exctype, value = sys.exc_info()[:2] 
                
                logger.error("""Error trying to send message:(chat:%s,text:%s,parse_mode:%s,disable_preview:%s,
                             reply_keyboard:%s, reply_to_message_id:%s): %s:%s""" % 
                             (chat_id, chunk_text, parse_mode, disable_web_page_preview, keyboard_to_send, reply_to_message_id, exctype, value))
                
            
@python_2_unicode_compatible
class KikBot(IntegrationBot):    
    api_key = models.CharField(_('Kik Bot API key'), max_length=200, db_index=True)
    username = models.CharField(_("Kik Bot User name"), max_length=200)
   
    class Meta:
        verbose_name = _('Kik Bot')
        verbose_name_plural = _('Kik Bots')    
    
    def __init__(self, *args, **kwargs):
        super(KikBot, self).__init__(*args, **kwargs)
        self._bot = None
        if self.api_key and self.username:
            self.init_bot()
           
    def __str__(self):
        return "%s" % self.username
    
    def __repr__(self):
        return "(%s, %s)" % (self.username, self.api_key)
    
    def init_bot(self):
        self._bot = KikApi(self.username, self.api_key)
    
    def set_webhook(self, url):
        self._bot.set_configuration(Configuration(webhook=url))
    
    @property
    def hook_url(self):
        return 'microbot:kikbot'
    
    @property
    def hook_id(self):
        return str(self.id)
    
    @property
    def null_url(self):
        return "https://example.com"
    
    @property
    def identity(self):
        return 'kik'
    
    def message_text(self, message):
        return message.body
    
    def get_chat_state(self, message):
        try:
            return KikChatState.objects.get(chat=message.chat, user=message.from_user, state__bot=self.bot)
        except KikChatState.DoesNotExist:
            return None
        
    def build_keyboard(self, keyboard):     
        def traverse(o, tree_types=(list, tuple)):
            if isinstance(o, tree_types):
                for value in o:
                    for subvalue in traverse(value, tree_types):
                        yield subvalue
            else:
                yield o
                
        built_keyboard = []
        if keyboard:
            built_keyboard = [TextResponse(element) for element in traverse(ast.literal_eval(keyboard))][:20]           
        return built_keyboard
    
    def create_chat_state(self, message, target_state, context):
        KikChatState.objects.create(chat=message.chat,
                                    user=message.from_user,
                                    state=target_state,
                                    ctx=context)

    def get_chat_id(self, message):
        return message.chat.id
    
    def send_message(self, chat_id, text, keyboard, reply_message=None, user=None):
        if reply_message:
            to = reply_message.from_user.username
        if user:
            to = user
        msgs = []
        for chunk_text, last in self.batch(text, 100):
            msg = TextMessage(to=to, chat_id=chat_id, body=chunk_text)
            if last and keyboard:
                msg.keyboards.append(SuggestedResponseKeyboard(to=to, responses=keyboard))
            msgs.append(msg)
        try:
            logger.debug("Messages to send:(%s)" % str([m.to_json() for m in msgs]))
            self._bot.send_messages(msgs)    
            logger.debug("Message sent OK:(%s)" % str([m.to_json() for m in msgs]))
        except:
            exctype, value = sys.exc_info()[:2] 
            logger.error("Error trying to send message:(%s): %s:%s" % (str([m.to_json() for m in msgs]), exctype, value))