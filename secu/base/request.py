from tornado.web import RequestHandler
import json
from importlib import import_module
from datetime import datetime

from common.json import j, jj, plus
from common.db import DB

from session.controls import Session


def JsonResponse(hander, code, data=None, msg=None):
    hander.write({'code': code, 'msg': msg, 'data': data})


class BaseHandler(RequestHandler):

    @property
    def db(self):
        if not self._db:
            app = import_module(self.__module__.split('.')[0])
            conf = import_module('config')
            connection = conf.DATABASES[app.database][conf.TEST]
            self._db = DB(**connection).session
        return self._db

    def prepare(self):
        self._db = None
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_params()

    def on_finish(self):
        if self._db:
            self._db.close()

        self.session.dispose()

    def options(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
        self.set_header('Access-Control-Max-Age', 86400)
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, X_Requested_With, Content-Type, Accept')

    def set_params(self):
        self.GET, self.POST = {}, {}

        for k, v in self.request.query_arguments.items():
            self.GET[k] = v[-1].decode()

        if self.request.headers.get('Content-Type') == 'application/json':
            if self.request.body:
                self.POST = json.loads(self.request.body.decode())
        else:
            for k, v in self.request.body_arguments.items():
                self.POST[k] = v[-1].decode()   

        session_id = self.GET.get('session_id') if self.GET.get('session_id') else self.get_cookie('session_id')
        self.session = Session(session_id=session_id)

        if self.request.method == 'POST':            
            self.POST['entry_user'] = self.session['userid'] 
                  
        self.GETPOST = plus(self.GET, self.POST)        