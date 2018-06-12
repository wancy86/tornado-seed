import config as conf
from importlib import import_module as im
import tornado.web as web
import os

def get_application():
    urlpatterns = []

    for app in conf.INSTALLED_APPS:
        cmd = app + '.urls' 
        urlpatterns = urlpatterns + getattr(im(cmd), 'urlpatterns')    
        
    return web.Application(
        urlpatterns,
        debug=conf.DEBUG,
    )