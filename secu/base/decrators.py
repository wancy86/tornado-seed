import functools
import json
import traceback

import config
from common.emailhelper import send_email
from .request import JsonResponse
from common.form import InvalidException
import config as conf


def authenticated(fn):
    @functools.wraps(fn)
    def _fn(handler):
        if handler.session['userid']:
            try:
                fn(handler)
            except InvalidException as e:
                return JsonResponse(handler, '100', msg=str(e))
            except Exception as e:
                handler.db.rollback()
                raise e
                # for receivers in config.ERROR_REPORT_RECEIVERS:
                #     msg = 'USERID:{0}<br/><br/>URI:{1}<br/><br/>METHOD:{2}<br/><br/>GETPOST:{3}<br/><br/>ERROR info:{4}'
                #     msg = msg.format(handler.session['userid'], handler.request.uri, handler.request.method,
                #                      json.dumps(handler.GETPOST), str(traceback.format_exc()))
                #     msg = msg.replace('\n', '<br/>')
                #     send_email(receivers, 'error', msg)
                # return JsonResponse(handler, '500', msg='')
            finally:
                pass
        else:
            return JsonResponse(handler, '200', msg='登陆已超时，请重新登录！')

    return _fn


def handle_request_exception(fn):
    @functools.wraps(fn)
    def _fn(handler):
        try:
            fn(handler)
        except InvalidException as e:
            return JsonResponse(handler, '100', msg=str(e))
        except Exception as e:
            handler.db.rollback()
            for receivers in config.ERROR_REPORT_RECEIVERS:
                msg = '<br/>URI:{0}<br/><br/>METHOD:{1}<br/><br/>GETPOST:{2}<br/><br/>ERROR info:{3}'
                msg = msg.format(handler.request.uri, handler.request.method, json.dumps(handler.GETPOST), str(traceback.format_exc()))
                msg = msg.replace('\n', '<br/>')
                send_email(receivers, 'error', msg)
            return JsonResponse(handler, '500', msg='系统繁忙，请稍候再试！')
        finally:
            pass

    return _fn
