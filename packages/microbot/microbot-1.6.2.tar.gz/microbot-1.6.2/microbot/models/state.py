# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
import logging
from microbot.models.base import MicrobotModel
from microbot.models import TelegramChat, KikChat, KikUser, TelegramUser
import json

logger = logging.getLogger(__name__)

@python_2_unicode_compatible    
class State(MicrobotModel):    
    name = models.CharField(_('State name'), db_index=True, max_length=255, 
                            help_text=_("Name of the state"))
    bot = models.ForeignKey('Bot', verbose_name=_('Bot'), related_name='states',
                            help_text=_("Bot which state is attached to"))  
    
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')

    def __str__(self):
        return "%s" % self.name
    

class AbsChatState(MicrobotModel):
    context = models.TextField(verbose_name=_("Context"),
                               help_text=_("Context serialized to json when this state was set"), null=True, 
                               blank=True)
    state = models.ForeignKey(State, verbose_name=_('State'), related_name='%(class)s_chat',
                              help_text=_("State related to the chat"))

    class Meta:
        abstract = True
        
    def _get_context(self):
        if self.context:
            return json.loads(self.context)
        return {}
    
    def _set_context(self, value):
        self.context = json.dumps(value)        
    
    ctx = property(_get_context, _set_context)


@python_2_unicode_compatible    
class TelegramChatState(AbsChatState):
    chat = models.ForeignKey(TelegramChat, db_index=True, verbose_name=_('Chat'), related_name='telegram_chatstates',
                             help_text=_("Chat in Telegram API format. https://core.telegram.org/bots/api#chat"))
    user = models.ForeignKey(TelegramUser, db_index=True, verbose_name=_("Telegram User"), related_name='telegram_chatstates',
                             help_text=_("Telegram unique username"))

    class Meta:
        verbose_name = _('Telegram Chat State')
        verbose_name = _('Telegram Chats States')
        
    def __str__(self):
        return "(%s:%s)" % (str(self.chat.id), self.state.name)
    
    
@python_2_unicode_compatible    
class KikChatState(AbsChatState):
    chat = models.ForeignKey(KikChat, db_index=True, verbose_name=_('Kik Chat'), related_name='kik_chatstates',
                             help_text=_("Chat in Kik API format. https://dev.kik.com/#/docs/messaging#authentication"))
    user = models.ForeignKey(KikUser, db_index=True, verbose_name=_("Kik User"), related_name='kik_chatstates',
                             help_text=_("Kik unique username"))
    
    class Meta:
        verbose_name = _('Kik Chat State')
        verbose_name = _('Kik Chats States')
        unique_together = ('chat', 'user')
        
    def __str__(self):
        return "(%s:%s)" % (str(self.chat.id), self.state.name)