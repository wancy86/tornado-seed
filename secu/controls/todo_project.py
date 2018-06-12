from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import handle_request_exception, authenticated
from ..models import Project
from sqlalchemy import and_
from common.json import json_by_result


class ProjectHandler(BaseHandler):

    @authenticated
    def post(self):
        model = Project(**Project.Form(**self.POST).data)
        self.db.add(model)
        self.db.commit()
        return JsonResponse(self, '000', data=model.json)

    @authenticated
    def delete(self):
        model = self.db.query(Project).filter(Project.id == self.GETPOST['id']).first()
        if model:
            self.db.delete(model)
            self.db.commit()

        return JsonResponse(self, '000')

    @authenticated
    def put(self):
        model = self.db.query(Project).filter(Project.id == self.POST['id']).first()
        if model:
            model.update(**Project.Form(**self.POST).data)
            self.db.commit()
            return JsonResponse(self, '000', data=model.json)
        return JsonResponse(self, '001', msg="你要更新的记录不存在！")
            
    @authenticated
    def get(self):
        ACTION = self.GET.get('ACTION', '')
        if ACTION == 'ONE':
            pk = self.GET.get('id')
            if pk:
                model = self.db.query(Project).filter(Project.id == pk).first()
                if model:
                    return JsonResponse(self, '000', data=model.json)
                else:
                    return JsonResponse(self, '001', msg="你查询的记录不存在！")
            else:
                return JsonResponse(self, '100', msg="请传入参数id！")
        elif ACTION == 'QUERY':
            query = '''
                select p.id,
                       p.name,
                       p.desp,
                       p.cats,
                       p.statuses,
                       p.priorities,
                       p.entry_date,
                       u.fullname
                from todo_project as p
                left join secu_user as u on p.entry_user = u.id
                order by p.identity desc; 
            '''
            data = json_by_result(self.db.execute(query).fetchall())
            return JsonResponse(self, '000', data=data)
        elif ACTION == 'OPTIONS':
            return JsonResponse(self, '000', data=Project.options)
        else:
            return JsonResponse(self, '100', msg="缺失参数ACTION")
