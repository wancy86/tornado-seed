from secu.models import FavoriteItem
from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import handle_request_exception, authenticated
from sqlalchemy import and_
from common.json import json_by_result


class FavoriteItemHandler(BaseHandler):

    @authenticated
    def post(self):
        model = self.db.query(FavoriteItem).filter(
            and_(FavoriteItem.userid == self.session['userid'], FavoriteItem.itemid == self.GETPOST['itemid'])).first()
        if model:
            return JsonResponse(self, '000', data=model.json)
        else:
            self.POST['userid'] = self.session['userid']
            data = FavoriteItem.Form(**self.POST).data
            model = FavoriteItem(**data)
            self.db.add(model)
            self.db.commit()
            return JsonResponse(self, '000', data=model.json)

    @authenticated
    def delete(self):
        model = self.db.query(FavoriteItem).filter(
            and_(FavoriteItem.userid == self.session['userid'], FavoriteItem.itemid == self.GETPOST['itemid'])).first()
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
