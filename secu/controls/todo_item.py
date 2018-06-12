from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import handle_request_exception, authenticated
from ..models import Item, PersonInCharge
from sqlalchemy import and_
from common.json import json_by_result


class ItemHandler(BaseHandler):

    @authenticated
    def post(self):
        data = Item.Form(**self.POST).data
        person_in_charges = data['person_in_charges']
        del data['person_in_charges']

        model = Item(**data)
        self.db.add(model)
        self.db.flush()

        for x in person_in_charges:
            x['itemid'] = model.id
            self.db.add(PersonInCharge(**x))

        self.db.commit()
        return JsonResponse(self, '000', data=model.json)

    @authenticated
    def delete(self):
        model = self.db.query(Item).filter(Item.id == self.GETPOST['id']).first()
        if model:
            self.db.delete(model)
            ps = self.db.query(PersonInCharge).filter(PersonInCharge.itemid == self.GETPOST['id']).delete()
            self.db.commit()
            return JsonResponse(self, '000')
        else:
            return JsonResponse(self, '001', msg="你要删除的记录不存在！")

    @authenticated
    def put(self):
        data = Item.Form(**self.POST).data
        person_in_charges = data['person_in_charges']
        del data['person_in_charges']

        model = self.db.query(Item).filter(Item.id == self.POST['id']).first()
        if model:
            model.update(**Item.Form(**self.POST).data)
            ps = self.db.query(PersonInCharge).filter(PersonInCharge.itemid == self.POST['id']).delete()

            for x in person_in_charges:
                x['itemid'] = model.id
                self.db.add(PersonInCharge(**x))

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
                model = self.db.query(Item).filter(Item.id == pk).first()
                if model:
                    ps = self.db.query(PersonInCharge).filter(PersonInCharge.itemid == pk).order_by(
                        PersonInCharge.sequence.asc()).all()
                    data = model.json
                    data['person_in_charges'] = [i.json for i in ps]
                    return JsonResponse(self, '000', data=data)
                else:
                    return JsonResponse(self, '001', msg="你查询的记录不存在！")
            else:
                return JsonResponse(self, '100', msg="请传入参数id！")
        elif ACTION == 'QUERY':
            query = '''
                select p.id,
                       p.projectid,
                       pro.name as projectname,
                       p.title, -- 名称
                       p.cat, -- 类别
                       p.priority, -- 优先级
                       p.status, -- 当前状态
                       u.fullname as person_in_charge, -- 当前负责人
                       p.estimated_duration, -- 预估时间
                       p.entry_date, -- 创建时间
                       cu.fullname as create_user, -- 创建人
                       case when uw.itemid is not null then 1 else 0 end as isunderway,
                       case when f.itemid is not null then 1 else 0 end as isfavorite
                from todo_item as p
                left join todo_project as pro on p.projectid=pro.id
                left join todo_person_in_charge as c on p.id = c.itemid and
                                                        p.status = c.itemstatus 
                left join secu_user as u on c.person_in_charge = u.id
                left join secu_user as cu on p.entry_user = cu.id
                left join todo_underway as uw on uw.itemid = p.id and uw.userid = :current_user
                left join todo_favorite_item as f on f.itemid = p.id and f.userid = :current_user
                where (:title = '' or p.title like :title) and
                      (:projectid = '' or p.projectid = :projectid) and
                      (:status = '' or p.status = :status) and
                      (:person_in_charge = '' or c.person_in_charge = :person_in_charge) and
                      (:cat = '' or p.cat = :cat) and
                      (:priority = '' or p.priority = :priority) and
                      (p.estimated_duration >= :min_estimated_duration) and
                      (p.estimated_duration <= :max_estimated_duration) and
                      (p.entry_date >= :min_entry_date) and
                      (p.entry_date <= :max_entry_date)
                order by p.identity desc limit {},{} ;
            '''

            count_query = '''
                select count(1)
                from todo_item as p
                left join todo_person_in_charge as c on p.id = c.itemid and
                                                        p.status = c.itemstatus 
                left join secu_user as u on c.person_in_charge = u.id
                left join secu_user as cu on p.entry_user = cu.id
                left join todo_underway as uw on uw.itemid = p.id and uw.userid = :current_user
                left join todo_favorite_item as f on f.itemid = p.id and f.userid = :current_user
                where (:title = '' or p.title like :title) and
                      (:projectid = '' or p.projectid = :projectid) and
                      (:status = '' or p.status = :status) and
                      (:person_in_charge = '' or c.person_in_charge = :person_in_charge) and
                      (:cat = '' or p.cat = :cat) and
                      (:priority = '' or p.priority = :priority) and
                      (p.estimated_duration >= :min_estimated_duration) and
                      (p.estimated_duration <= :max_estimated_duration) and
                      (p.entry_date >= :min_entry_date) and
                      (p.entry_date <= :max_entry_date);
            '''

            condition = {
                'title': '' if not self.GET.get('title') else '%{}%'.format(self.GET.get('title')),
                'projectid': self.GET.get('projectid', ''),
                'status': self.GET.get('status', ''),
                'person_in_charge': self.GET.get('person_in_charge', ''),
                'cat': self.GET.get('cat', ''),
                'priority': self.GET.get('priority', ''),
                'min_estimated_duration': int(self.GET.get('min_estimated_duration', 0)),
                'max_estimated_duration': int(self.GET.get('max_estimated_duration', 999999)),
                'min_entry_date': self.GET.get('min_entry_date', '1900-1-1'),
                'max_entry_date': self.GET.get('max_entry_date', '2100-1-1'),
                'current_user': self.session['userid']
            }

            record = self.GET.get('record')
            pagesize = self.GET.get('pagesize', '10')
            if not record:
                record = int(self.GET.get('pageindex', 0)) * int(pagesize)

            query = query.format(record, pagesize)

            count = self.db.execute(count_query, condition).scalar()
            data = json_by_result(self.db.execute(query, condition).fetchall())

            return JsonResponse(self, '000', data={'count': count, 'list': data})
        elif ACTION == 'MYITEMS':
            query = '''
                select p.id,
                       p.projectid,
                       pro.name as projectname,
                       p.title, -- 名称
                       p.cat, -- 类别
                       p.priority, -- 优先级
                       p.status, -- 当前状态
                       u.fullname as person_in_charge, -- 当前负责人
                       p.estimated_duration, -- 预估时间
                       p.entry_date, -- 创建时间
                       cu.fullname as create_user, -- 创建人
                       case when uw.itemid is not null then 1 else 0 end as isunderway,
                       case when f.itemid is not null then 1 else 0 end as isfavorite
                from todo_item as p
                left join todo_project as pro on p.projectid=pro.id
                left join todo_person_in_charge as c on p.id = c.itemid and
                                                        p.status = c.itemstatus 
                left join secu_user as u on c.person_in_charge = u.id
                left join secu_user as cu on p.entry_user = cu.id
                left join todo_underway as uw on uw.itemid = p.id and uw.userid = :current_user
                left join todo_favorite_item as f on f.itemid = p.id and f.userid = :current_user
                where p.id in (select distinct itemid from todo_person_in_charge where person_in_charge = :current_user) and 
                      (:title = '' or p.title like :title) and
                      (:projectid = '' or p.projectid = :projectid) and
                      (:status = '' or p.status = :status) and
                      (:person_in_charge = '' or c.person_in_charge = :person_in_charge) and
                      (:cat = '' or p.cat = :cat) and
                      (:priority = '' or p.priority = :priority) and
                      (p.estimated_duration >= :min_estimated_duration) and
                      (p.estimated_duration <= :max_estimated_duration) and
                      (p.entry_date >= :min_entry_date) and
                      (p.entry_date <= :max_entry_date)
                order by p.identity desc limit {},{} ;
            '''

            count_query = '''
                select count(1)
                from todo_item as p
                left join todo_person_in_charge as c on p.id = c.itemid and
                                                        p.status = c.itemstatus 
                left join secu_user as u on c.person_in_charge = u.id
                left join secu_user as cu on p.entry_user = cu.id
                left join todo_underway as uw on uw.itemid = p.id and uw.userid = :current_user
                left join todo_favorite_item as f on f.itemid = p.id and f.userid = :current_user
                where p.id in (select distinct itemid from todo_person_in_charge where person_in_charge = :current_user) and 
                      (:title = '' or p.title like :title) and
                      (:projectid = '' or p.projectid = :projectid) and
                      (:status = '' or p.status = :status) and
                      (:person_in_charge = '' or c.person_in_charge = :person_in_charge) and
                      (:cat = '' or p.cat = :cat) and
                      (:priority = '' or p.priority = :priority) and
                      (p.estimated_duration >= :min_estimated_duration) and
                      (p.estimated_duration <= :max_estimated_duration) and
                      (p.entry_date >= :min_entry_date) and
                      (p.entry_date <= :max_entry_date);
            '''

            condition = {
                'title': '' if not self.GET.get('title') else '%{}%'.format(self.GET.get('title')),
                'projectid': self.GET.get('projectid', ''),
                'status': self.GET.get('status', ''),
                'person_in_charge': self.GET.get('person_in_charge', ''),
                'cat': self.GET.get('cat', ''),
                'priority': self.GET.get('priority', ''),
                'min_estimated_duration': int(self.GET.get('min_estimated_duration', 0)),
                'max_estimated_duration': int(self.GET.get('max_estimated_duration', 999999)),
                'min_entry_date': self.GET.get('min_entry_date', '1900-1-1'),
                'max_entry_date': self.GET.get('max_entry_date', '2100-1-1'),
                'current_user': self.session['userid']
            }

            record = self.GET.get('record')
            pagesize = self.GET.get('pagesize', '10')
            if not record:
                record = int(self.GET.get('pageindex', 0)) * int(pagesize)

            query = query.format(record, pagesize)

            count = self.db.execute(count_query, condition).scalar()
            data = json_by_result(self.db.execute(query, condition).fetchall())

            return JsonResponse(self, '000', data={'count': count, 'list': data})
        elif ACTION == 'UNDERWAY':
            query = '''
                select p.id,
                       p.projectid,
                       pro.name as projectname,
                       p.title, -- 名称
                       p.cat, -- 类别
                       p.priority, -- 优先级
                       p.status, -- 当前状态
                       u.fullname as person_in_charge, -- 当前负责人
                       p.estimated_duration, -- 预估时间
                       p.entry_date, -- 创建时间
                       cu.fullname as create_user, -- 创建人
                       u1.fullname as underway_user,
                       case when uw.itemid is not null then 1 else 0 end as isunderway,
                       case when f.itemid is not null then 1 else 0 end as isfavorite
                from 
                todo_underway as uw0
                left join todo_item as p on uw0.itemid = p.id
                left join todo_project as pro on p.projectid=pro.id
                left join todo_person_in_charge as c on p.id = c.itemid and
                                                        p.status = c.itemstatus 
                left join secu_user as u on c.person_in_charge = u.id
                left join secu_user as cu on p.entry_user = cu.id
                left join secu_user as u1 on uw0.userid = u1.id
                left join todo_underway as uw on uw.itemid = p.id and uw.userid = :current_user
                left join todo_favorite_item as f on f.itemid = p.id and f.userid = :current_user
                where (:title = '' or p.title like :title) and
                      (:projectid = '' or p.projectid = :projectid) and
                      (:status = '' or p.status = :status) and
                      (:person_in_charge = '' or c.person_in_charge = :person_in_charge) and
                      (:underway_user = '' or uw0.userid = :underway_user) and
                      (:cat = '' or p.cat = :cat) and
                      (:priority = '' or p.priority = :priority) and
                      (p.estimated_duration >= :min_estimated_duration) and
                      (p.estimated_duration <= :max_estimated_duration) and
                      (p.entry_date >= :min_entry_date) and
                      (p.entry_date <= :max_entry_date)
                order by uw0.itemid desc limit {},{} ;
            '''

            count_query = '''
                select count(1)
                from 
                todo_underway as uw0
                left join todo_item as p on uw0.itemid = p.id
                left join todo_person_in_charge as c on p.id = c.itemid and
                                                        p.status = c.itemstatus 
                left join secu_user as u on c.person_in_charge = u.id
                left join secu_user as cu on p.entry_user = cu.id
                left join secu_user as u1 on uw0.userid = u1.id
                left join todo_underway as uw on uw.itemid = p.id and uw.userid = :current_user
                left join todo_favorite_item as f on f.itemid = p.id and f.userid = :current_user
                where (:title = '' or p.title like :title) and
                      (:projectid = '' or p.projectid = :projectid) and
                      (:status = '' or p.status = :status) and
                      (:person_in_charge = '' or c.person_in_charge = :person_in_charge) and
                      (:underway_user = '' or uw0.userid = :underway_user) and
                      (:cat = '' or p.cat = :cat) and
                      (:priority = '' or p.priority = :priority) and
                      (p.estimated_duration >= :min_estimated_duration) and
                      (p.estimated_duration <= :max_estimated_duration) and
                      (p.entry_date >= :min_entry_date) and
                      (p.entry_date <= :max_entry_date);
            '''

            condition = {
                'title': '' if not self.GET.get('title') else '%{}%'.format(self.GET.get('title')),
                'projectid': self.GET.get('projectid', ''),
                'status': self.GET.get('status', ''),
                'person_in_charge': self.GET.get('person_in_charge', ''),
                'cat': self.GET.get('cat', ''),
                'priority': self.GET.get('priority', ''),
                'min_estimated_duration': int(self.GET.get('min_estimated_duration', 0)),
                'max_estimated_duration': int(self.GET.get('max_estimated_duration', 999999)),
                'min_entry_date': self.GET.get('min_entry_date', '1900-1-1'),
                'max_entry_date': self.GET.get('max_entry_date', '2100-1-1'),
                'current_user': self.session['userid'],
                'underway_user': self.GET.get('underway_user', '')
            }

            record = self.GET.get('record')
            pagesize = self.GET.get('pagesize', '10')
            if not record:
                record = int(self.GET.get('pageindex', 0)) * int(pagesize)

            query = query.format(record, pagesize)

            count = self.db.execute(count_query, condition).scalar()
            data = json_by_result(self.db.execute(query, condition).fetchall())

            return JsonResponse(self, '000', data={'count': count, 'list': data})
        elif ACTION == 'FAVORITE':
            query = '''
                select p.id,
                       p.projectid,
                       pro.name as projectname,
                       p.title, -- 名称
                       p.cat, -- 类别
                       p.priority, -- 优先级
                       p.status, -- 当前状态
                       u.fullname as person_in_charge, -- 当前负责人
                       p.estimated_duration, -- 预估时间
                       p.entry_date, -- 创建时间
                       cu.fullname as create_user, -- 创建人
                       case when uw.itemid is not null then 1 else 0 end as isunderway,
                       case when f.itemid is not null then 1 else 0 end as isfavorite
                from 
                todo_favorite_item as f0
                left join todo_item as p on f0.itemid = p.id
                left join todo_project as pro on p.projectid=pro.id
                left join todo_person_in_charge as c on p.id = c.itemid and
                                                        p.status = c.itemstatus 
                left join secu_user as u on c.person_in_charge = u.id
                left join secu_user as cu on p.entry_user = cu.id
                left join todo_underway as uw on uw.itemid = p.id and uw.userid = :current_user
                left join todo_favorite_item as f on f.itemid = p.id and f.userid = :current_user
                where f0.userid = :current_user and
                      (:title = '' or p.title like :title)
                order by f0.itemid desc;
            '''

            condition = {
                'title': '' if not self.GET.get('title') else '%{}%'.format(self.GET.get('title')),
                'current_user': self.session['userid']
            }

            data = json_by_result(self.db.execute(query, condition).fetchall())

            return JsonResponse(self, '000', data=data)
        elif ACTION == 'OPTIONS':
            return JsonResponse(self, '000', data=Item.options)
        else:
            return JsonResponse(self, '100', msg="缺失参数ACTION")
