from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import handle_request_exception, authenticated
from ..models import Work, PersonInCharge
from sqlalchemy import and_
from common.json import json_by_result


class WorkHandler(BaseHandler):

    @authenticated
    def post(self):
        model = Work(**Work.Form(**self.POST).data)
        self.db.add(model)
        self.db.commit()
        return JsonResponse(self, '000', data=model.json)

    @authenticated
    def delete(self):
        model = self.db.query(Work).filter(Work.id == self.GETPOST['id']).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return JsonResponse(self, '000')
        else:
            self.db.commit()
            return JsonResponse(self, '001', msg="你要删除的记录不存在！")

    @authenticated
    def put(self):
        data = Work.PutForm(**self.POST).data
        model = self.db.query(Work).filter(Work.id == self.POST['id']).first()
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
                model = self.db.query(Work).filter(Work.id == pk).first()
                if model:
                    return JsonResponse(self, '000', data=model.json)
                else:
                    return JsonResponse(self, '001', msg="你查询的记录不存在！")
            else:
                return JsonResponse(self, '100', msg="请传入参数id！")
        elif ACTION == 'QUERY':
            query = '''
                select w.id,
                       w.itemid, -- 任务ID
                       w.desp, -- 工作内容
                       w.duration, -- 消耗时间
                       w.entry_date, -- 创建时间
                       u.fullname as create_user -- 日志记录人
                from todo_work as w
                left join secu_user as u on w.entry_user = u.id
                where w.itemid = :itemid
                order by w.identity desc limit {},{} ;
            '''

            count_query = '''
                select count(1)
                from todo_work as w
                left join secu_user as u on w.entry_user = u.id
                where w.itemid = :itemid;
            '''

            condition = {
                'itemid': self.GET.get('itemid', ''),
            }

            record = self.GET.get('record')
            pagesize = self.GET.get('pagesize', '10')
            record = record if record else int(self.GET.get('pageindex', 0)) * int(pagesize)
            
            query = query.format(record, pagesize)
            count = self.db.execute(count_query, condition).scalar()
            data = json_by_result(self.db.execute(query, condition).fetchall())
            return JsonResponse(self, '000', data={'count': count, 'list': data})

        elif ACTION == 'MYLOGS':
            query = '''
                SELECT w.id,
                       w.desp, 
                       w.duration, 
                       w.entry_date, 
                       u.username, 
                       i.title,  
                       p.name as project_name 
                FROM todo_work w
                JOIN secu_user u ON w.entry_user=u.id
                LEFT JOIN todo_item i ON w.itemid=i.id
                LEFT JOIN todo_project p ON i.projectid=p.id
                where u.id = :userid and
                      (:projectid = '' or p.id = :projectid) and
                      (:item_name = '' or i.title like :item_name) and
                      (w.duration >= :min_duration) and
                      (w.duration <= :max_duration) and
                      datediff(w.entry_date,:min_entry_date)>=0 and
                      datediff(w.entry_date,:max_entry_date)<=0
                order by w.entry_date desc limit {},{} ;
            '''

            count_query = '''
                SELECT count(1)
                FROM todo_work w
                JOIN secu_user u ON w.entry_user=u.id
                LEFT JOIN todo_item i ON w.itemid=i.id
                LEFT JOIN todo_project p ON i.projectid=p.id
                where u.id = :userid and
                    (:projectid = '' or p.id = :projectid) and
                    (:item_name = '' or i.title like :item_name) and
                    (w.duration >= :min_duration) and
                    (w.duration <= :max_duration) and
                    datediff(w.entry_date,:min_entry_date)>=0 and
                    datediff(w.entry_date,:max_entry_date)<=0;
            '''

            condition = {
                'userid': self.GET.get('userid', self.session['userid']),
                'projectid': self.GET.get('projectid', ''),
                'item_name': '' if not self.GET.get('item_name') else '%{}%'.format(self.GET.get('item_name')),
                'min_duration': int(self.GET.get('min_duration', 0)),
                'max_duration': int(self.GET.get('max_duration', 999999)),
                'min_entry_date': self.GET.get('min_entry_date', '1900-1-1'),
                'max_entry_date': self.GET.get('max_entry_date', '2100-1-1')
            }

            record = self.GET.get('record')
            pagesize = self.GET.get('pagesize', '10')
            record = record if record else int(self.GET.get('pageindex', 0)) * int(pagesize)
            
            query = query.format(record, pagesize)
            count = self.db.execute(count_query, condition).scalar()
            self.db.commit()
            data = json_by_result(self.db.execute(query, condition).fetchall())
            return JsonResponse(self, '000', data={'count': count, 'list': data})

        else:
            return JsonResponse(self, '100', msg="缺失参数ACTION")
