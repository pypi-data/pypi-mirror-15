from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from microbot import views

urlpatterns = [
    url(r'^telegrambot/(?P<hook_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', 
        csrf_exempt(views.TelegramHookView.as_view()), name='telegrambot'),
    url(r'^kikbot/(?P<hook_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', 
        csrf_exempt(views.KikHookView.as_view()), name='kikbot'),       
    url(r'^hook/(?P<key>\w+)/$', csrf_exempt(views.MicrobotHookView.as_view()), name='hook')]
