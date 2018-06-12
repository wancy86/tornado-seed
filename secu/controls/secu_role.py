from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import handle_request_exception, authenticated
from ..models import Role
from sqlalchemy import and_
from common.json import json_by_result


class RoleHandler(BaseHandler):

    @authenticated
    def post(self):
        data = Role.Form(**self.POST).data
        model = Role(**data)
        self.db.add(model)

        self.db.commit()
        return JsonResponse(self, '000', data=model.json)

    @authenticated
    def delete(self):
        model = self.db.query(Role).filter(Role.id == self.GETPOST['id']).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return JsonResponse(self, '000')
        else:
            return JsonResponse(self, '001', msg="你要删除的记录不存在！")

    @authenticated
    def put(self):
        ACTION = self.GETPOST.get('ACTION')

        if ACTION == 'ROLE':
            data = Role.Form(**self.POST).data
            model = self.db.query(Role).filter(Role.id == self.POST['id']).first()
            if model:
                model.update(**data)
                self.db.commit()
                return JsonResponse(self, '000')
            else:
                return JsonResponse(self, '001', msg="你要更新的记录不存在！")
        elif ACTION == 'ADD-RIGHT':
            model = self.db.query(Role).filter(Role.id == self.POST['id']).first()
            if model:
                if not model.rights:
                    model.rights = self.POST['right']
                else:
                    model.rights = model.rights + ',' + self.POST['right']
                self.db.commit()
                return JsonResponse(self, '000')
            else:
                return JsonResponse(self, '001', msg="你要更新的记录不存在！")
        elif ACTION == 'REMOVE-RIGHT':
            model = self.db.query(Role).filter(Role.id == self.POST['id']).first()
            if model:
                model.rights = model.rights.replace(',' + self.POST['right'], '').replace(self.POST['right'], '')
                self.db.commit()
                return JsonResponse(self, '000')
            else:
                return JsonResponse(self, '001', msg="你要更新的记录不存在！")

    @authenticated
    def get(self):
        ACTION = self.GET.get('ACTION')
        if ACTION == 'ONE':
            pk = self.GET.get('id')
            if pk:
                model = self.db.query(Role).filter(Role.id == pk).first()
                if model:
                    return JsonResponse(self, '000', data=model.json)
                else:
                    return JsonResponse(self, '001', msg="你查询的记录不存在！")
            else:
                return JsonResponse(self, '100', msg="请传入参数id！")
        elif ACTION == 'RIGHTS':
            pk = self.GET.get('id')
            if pk:
                model = self.db.query(Role).filter(Role.id == pk).first()
                rights = model.rights if model else ''
                query = '''
                    select id,
                           name,
                           description,
                           case when locate(id, :rights) > 0 then 1 else 0 end as ishave
                    from secu_right order by id;
                '''
                result = json_by_result(self.db.execute(query, {'id': pk, 'rights': rights}).fetchall())
                return JsonResponse(self, '000', data=result)
            else:
                return JsonResponse(self, '100', msg="请传入参数id！")
        elif ACTION == 'QUERY':
            result = self.db.query(Role).all()
            return JsonResponse(self, '000', data=[r.json for r in result])
        else:
            return JsonResponse(self, '100', msg="缺失参数ACTION")
