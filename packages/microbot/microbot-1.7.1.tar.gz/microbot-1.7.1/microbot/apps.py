from django.apps import AppConfig
from django.apps import apps
from django.db.models import signals

def connect_bot_signals():
    from . import signals as handlers
    sender = apps.get_model("microbot", "Bot")
    signals.post_delete.connect(handlers.delete_bot_integrations,
                                sender=sender,
                                dispatch_uid="bot_delete_integrations")
    signals.post_save.connect(handlers.delete_cache,
                              sender=sender,
                              dispatch_uid='bot_delete_cache')
    signals.post_delete.connect(handlers.delete_cache,
                                sender=sender,
                                dispatch_uid='bot_delete_cache')    
    
def connect_telegram_bot_signals():
    from . import signals as handlers
    sender = apps.get_model("microbot", "TelegramBot")
    signals.pre_save.connect(handlers.validate_bot,
                             sender=sender,
                             dispatch_uid='telegram_bot_validate')
    signals.pre_save.connect(handlers.set_bot_webhook,
                             sender=sender,
                             dispatch_uid='telegram_bot_set_webhook')
    signals.pre_save.connect(handlers.set_bot_api_data,
                             sender=sender,
                             dispatch_uid='telegram_bot_set_api_data')
    signals.post_save.connect(handlers.delete_cache,
                              sender=sender,
                              dispatch_uid='telegram_bot_delete_cache')
    signals.post_delete.connect(handlers.delete_cache,
                                sender=sender,
                                dispatch_uid='telegram_bot_delete_cache')
    
def connect_kik_bot_signals():
    from . import signals as handlers
    sender = apps.get_model("microbot", "KikBot")
    signals.pre_save.connect(handlers.set_bot_webhook,
                             sender=sender,
                             dispatch_uid='kik_bot_set_webhook')
    signals.post_save.connect(handlers.delete_cache,
                              sender=sender,
                              dispatch_uid='kik_bot_delete_cache')
    signals.post_delete.connect(handlers.delete_cache,
                                sender=sender,
                                dispatch_uid='kik_bot_delete_cache')
    
def connect_messenger_bot_signals():
    from . import signals as handlers
    sender = apps.get_model("microbot", "MessengerBot")
    signals.pre_save.connect(handlers.set_bot_webhook,
                             sender=sender,
                             dispatch_uid='messenger_bot_set_webhook')
    signals.post_save.connect(handlers.delete_cache,
                              sender=sender,
                              dispatch_uid='messenger_bot_delete_cache')
    signals.post_delete.connect(handlers.delete_cache,
                                sender=sender,
                                dispatch_uid='messenger_bot_delete_cache')
    
def connect_telegram_api_signals():
    from . import signals as handlers
    chat = apps.get_model("microbot", "Chat")
    user = apps.get_model("microbot", "User")
    signals.post_save.connect(handlers.delete_cache,
                              sender=chat,
                              dispatch_uid='telegram_chat_delete_cache')
    signals.post_save.connect(handlers.delete_cache,
                              sender=user,
                              dispatch_uid='telegram_user_delete_cache')
    signals.post_delete.connect(handlers.delete_cache,
                                sender=chat,
                                dispatch_uid='telegram_chat_delete_cache')
    signals.post_delete.connect(handlers.delete_cache,
                                sender=user,
                                dispatch_uid='telegram_user_delete_cache')
    
def connect_kik_api_signals():
    from . import signals as handlers
    user = apps.get_model("microbot", "KikUser")
    signals.post_save.connect(handlers.delete_cache,
                              sender=user,
                              dispatch_uid='kik_user_delete_cache')
    signals.post_delete.connect(handlers.delete_cache,
                                sender=user,
                                dispatch_uid='kik_user_delete_cache')

    
def connect_environment_vars_signals():
    from . import signals as handlers
    environment_var = apps.get_model("microbot", "EnvironmentVar")
    signals.post_save.connect(handlers.delete_cache_env_vars,
                              sender=environment_var,
                              dispatch_uid='environment_related_to_bot_delete_cache')
    signals.post_delete.connect(handlers.delete_cache_env_vars,
                                sender=environment_var,
                                dispatch_uid='environment_related_to_bot_delete_cache')

class MicrobotAppConfig(AppConfig):
    name = "microbot"
    verbose_name = "Microbot"

    def ready(self):
        connect_bot_signals()
        connect_telegram_bot_signals()
        connect_kik_bot_signals()
        connect_messenger_bot_signals()
        connect_telegram_api_signals()
        connect_kik_api_signals()
        connect_environment_vars_signals()