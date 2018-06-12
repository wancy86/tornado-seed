from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import handle_request_exception
from ..models import User
from sqlalchemy import and_


class LoginHandler(BaseHandler):

    @handle_request_exception
    def post(self):
        data = User.LoginForm(**self.POST).data
        user = self.db.query(User).filter(and_(User.mobile == data['mobile'], User.pwd == data['pwd'])).first()
        if user:
            self.session.abandon()
            self.session['userid'] = user.id
            data = user.json
            data['session_id'] = self.session.session_id
            return JsonResponse(self, '000', data=data)
        else:
            return JsonResponse(self, '001', msg="用户名或者密码不正确")    
