import sys
import re
from importlib import import_module

import config as conf
import common

template = '''
import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, Integer, Boolean

from .__basemodel__ import Model, Column 
import common.form as form

class <classname>(Model):
    __tablename__ = '<tablename>'

'''

class Space(object):
    def __getitem__(self, key=4):
        return ''.join([' ' for x in range(key)])

class Gen(object):
    def __init__(self, app_name, table_name=''):
        self.template = template
        self.space = Space()
        app = import_module(app_name)
        
        self.app_name = app_name
        self.database = app.database
        self.table_name = table_name

        self.db = common.db.DB(**conf.DATABASES[app.database][0]).session

        if table_name:
            self.build_model(table_name)


    def build_model(self, table_name):
        query = '''
            select COLUMN_NAME, 
                   DATA_TYPE, 
                   CHARACTER_MAXIMUM_LENGTH,
                   COLUMN_KEY,
                   EXTRA,
                   COLUMN_COMMENT
            from information_schema.columns
            where table_schema = :database and table_name = :table_name
        '''
        condition = {
            'database': self.database,
            'table_name': self.table_name
        }

        cols = common.json.json_by_result(self.db.execute(query, condition).fetchall())
        self.db.commit()

        class_name = ''.join([ name.capitalize() for name in self.table_name.split('_')])
        self.template = self.template.replace('<classname>', class_name)
        self.template = self.template.replace('<tablename>', self.table_name)

        path = 'F:/qqtr/cs/service/todo_work.py'
        with open(path, 'w', encoding='utf8') as f:
            f.write(self.template)

            # 创建列属性
            for col in cols:
                if col['COLUMN_NAME'] not in ('entry_user', 'entry_date'):
                    f.write(self.space[4])
                    line = '{0} = {1}'.format(col['COLUMN_NAME'], self.build_column(col))
                    f.write(line)
                    f.write('\n')  
                    print(col)  

            f.write('\n')  
            f.write(self.space[4])
            f.write('class Form(form.Form):')  
            f.write('\n')      
            # 创建表单
            for col in cols:
                if col['COLUMN_NAME'] not in ('entry_date'):
                    f.write(self.space[8])
                    line = '{0} = {1}'.format(col['COLUMN_NAME'], self.build_form_element(col))
                    f.write(line)
                    f.write('\n')  
                    print(col)          

    def build_column(self, col):
        if col['DATA_TYPE'] == 'varchar':
            params = 'String({0})'.format(col['CHARACTER_MAXIMUM_LENGTH'])
        elif col['DATA_TYPE'] == 'int':
            params = 'Integer' 
            if col['EXTRA'] == 'auto_increment':
                params = params + ', autoincrement=True'
        elif col['DATA_TYPE'] == 'datetime':
            params = 'Integer' 
            if col['EXTRA'] == 'auto_increment':
                params = params + ', autoincrement=True'                
        else:
            params = ''

        if col['COLUMN_KEY'] == 'PRI':
            if col['CHARACTER_MAXIMUM_LENGTH'] == '32':
                params = params + ', default=lambda: str(uuid.uuid4()).replace("-", "")'
            elif col['CHARACTER_MAXIMUM_LENGTH'] == '36':
                params = params + ', default=lambda: str(uuid.uuid4())'   

            params = params + ', primary_key=True'

        column = 'Column({0})'.format(params)

        return column                

    def build_form_element(self, col):
        if col['DATA_TYPE'] == 'varchar':
            params = 'form.String({0})'.format(col['COLUMN_COMMENT'])
        elif col['DATA_TYPE'] == 'int':
            params = 'form.Integer({0})'.format(col['COLUMN_COMMENT'])
        elif col['DATA_TYPE'] == 'datetime':
            params = 'form.String({0})'.format(col['COLUMN_COMMENT'])               
        else:
            params = ''

        if col['COLUMN_KEY'] == 'PRI':
            if col['CHARACTER_MAXIMUM_LENGTH'] in('32', '36'):
                params = params + ', default=lambda: str(uuid.uuid4()).replace("-", "")'
            params = params + ', primary_key=True'

        column = 'Column({0})'.format(params)

        return column         

def sys_argv_to_dict(sys_argv):
    args = {}
    for arg in sys_argv[1:]:
        m = re.match('^(\w+)=(\w*)$', arg)
        if m:
            key = m.group(1)
            value = m.group(2)
            args[key] = value
    return args




if __name__ == '__main__':
    args = sys_argv_to_dict(sys.argv)

    app_name = args.get('app')
    table_name = args.get('table')

    if app_name:
        Gen(app_name, table_name)
    else:
        print('请传递系统参数:app!')    
