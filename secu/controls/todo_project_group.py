from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import handle_request_exception, authenticated
from ..models import ProjectGroup
from sqlalchemy import and_
from common.json import json_by_result


class ProjectGroupHandler(BaseHandler):

    @authenticated
    def post(self):
        data = ProjectGroup.Form(**self.POST).data
        model = ProjectGroup(**data)
        self.db.add(model)
        self.db.commit()

        return JsonResponse(self, '000', data=model.json)

    @authenticated
    def delete(self):
        model = self.db.query(ProjectGroup).filter(and_(ProjectGroup.userid == self.GETPOST['userid'], ProjectGroup.projectid == self.GETPOST['projectid'])).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return JsonResponse(self, '000')
        else:
            return JsonResponse(self, '001', msg="你要删除的记录不存在！")

    @authenticated
    def get(self):
        ACTION = self.GET.get('ACTION', '')
        if ACTION == 'GET-GROUP-USERS':
            query = '''
                select pg.identity,
                       pg.projectid,
                       pg.userid,
                       u.fullname
                from todo_project_group as pg
                left join secu_user as u on pg.userid = u.id
                where projectid = :projectid;
            '''
            result = json_by_result(self.db.execute(query, {'projectid': self.GETPOST['projectid']}).fetchall())
            return JsonResponse(self, '000', data=result)
        else:
            return JsonResponse(self, '100', msg="缺失参数ACTION")
