from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import handle_request_exception, authenticated
from ..models import Underway
from sqlalchemy import and_
from common.json import json_by_result


class UnderwayHandler(BaseHandler):

    @authenticated
    def post(self):
        self.POST['userid'] = self.session['userid']
        data = Underway.Form(**self.POST).data
        model = Underway(**data)
        query = '''
        delete from todo_underway where userid = :userid
        '''
        self.db.execute(query, {"userid": self.session['userid']})
        self.db.add(model)
        self.db.commit()
        return JsonResponse(self, '000', data=model.json)

    @authenticated
    def delete(self):
        model = self.db.query(Underway).filter(
            and_(Underway.userid == self.session['userid'], Underway.itemid == self.GETPOST['itemid'])).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return JsonResponse(self, '000')
        else:
            return JsonResponse(self, '001', msg="你要删除的记录不存在！")

    @authenticated
    def put(self):
        pass

    @authenticated
    def get(self):
        pass
