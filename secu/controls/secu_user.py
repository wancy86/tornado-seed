from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import handle_request_exception, authenticated
from ..models import User
from sqlalchemy import and_
from common.json import json_by_result
from functools import reduce


class UserHandler(BaseHandler):

    @authenticated
    def post(self):
        data = User.Form(**self.POST).data
        model = User(**data)
        self.db.add(model)

        self.db.commit()
        return JsonResponse(self, '000', data=model.json)

    @authenticated
    def delete(self):
        model = self.db.query(User).filter(User.id == self.GETPOST['id']).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return JsonResponse(self, '000')
        else:
            return JsonResponse(self, '001', msg="你要删除的记录不存在！")

    @authenticated
    def put(self):
        data = User.Form(**self.POST).data
        model = self.db.query(User).filter(User.id == self.POST['id']).first()
        if model:
            model.update(**data)
            self.db.commit()
            return JsonResponse(self, '000')
        else:
            return JsonResponse(self, '001', msg="你要更新的记录不存在！")

    @authenticated
    def get(self):
        ACTION = self.GET.get('ACTION', '')
        if ACTION == 'ONE':
            pk = self.GET.get('id')
            if pk:
                model = self.db.query(User).filter(User.id == pk).first()
                if model:
                    return JsonResponse(self, '000', data=model.json)
                else:
                    return JsonResponse(self, '001', msg="你查询的记录不存在！")
            else:
                return JsonResponse(self, '100', msg="请传入参数id！")
        elif ACTION == 'QUERY':
            query = '''
                select u.id,
                       u.username, -- 用户名
                       u.fullname, -- 姓名
                       u.email, -- 邮箱
                       u.mobile, -- 手机号
                       r.name as rolename, -- 角色名称
                       u.entry_date -- 添加时间
                from secu_user as u
                left join secu_role as r on u.roles = r.id       
                order by u.fullname;
            '''

            data = json_by_result(self.db.execute(query).fetchall())

            return JsonResponse(self, '000', data=data)
        elif ACTION == 'SELF':
            pk = self.session['userid']
            query = '''
                select
                      u.fullname,
                      u.roles,
                      r.rights
                from secu_user u 
                left join secu_role r on u.roles = r.id
                where u.id = :id;
            '''
            data = json_by_result(self.db.execute(query, {'id': pk}).fetchall())

            return JsonResponse(self, '000', data=data)
        else:
            return JsonResponse(self, '100', msg="缺失参数ACTION")
