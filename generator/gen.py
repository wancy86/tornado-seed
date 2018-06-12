from importlib import import_module as im
from sqlalchemy import inspect
from sqlalchemy import and_
import os
import re
import sys
import shutil
import common.form as form

from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line

class Space(object):
    def __getitem__(self, key):
        return ''.join([' ' for x in range(key)])


class Gen:
    space = Space()

    def __init__(self, model_full_name, force=False, *args, **kwargs):

        if model_full_name == '':
            raise Exception('Please supply a valid full name of model.')

        names = model_full_name.split('.')
        self.force = force

        self.app_name = names[0]
        self.model_name = names[-1]
        self.module_name = ".".join(names[:-1])

        self.dirname = os.path.dirname(__file__)
        self.app_path = os.path.dirname(os.path.dirname(__file__))

        self.module = im(self.module_name)
        self.model = getattr(self.module, self.model_name)
        self.table = self.model.__table__
        self.columns = [col for col in self.table.columns if col.name not in ('entry_user', 'entry_date')]
        self.autoincrement = [col for col in self.table.columns if col.autoincrement == True]
        self.primary_keys = [col for col in self.columns if col.primary_key]

    def help_build_filter(self, method):
        pk_filter = ['{0}.{1} == self.{2}["{1}"]'.format(self.model_name, item.name, method) for item in self.primary_keys]
        return pk_filter[0] if len(pk_filter) == 1 else '{0}({1})'.format('and_', ', '.join(pk_filter))

class TestGen(Gen):

    def __init__(self, model_full_name, force=False, *args, **kwargs):
        super().__init__(model_full_name, force, *args, **kwargs)

        condition = ' and '.join([ '{0} = :{0}'.format(item.name) for item in self.primary_keys])
        self.CHECKSQL = 'select count(0) from {0} where {1}'.format(self.table.name, condition)

        # 如果不存在则创建对应的包
        model_test_dir = os.path.join(self.app_path, self.app_name, 'tests', self.model_name.lower())
        if not os.path.exists(model_test_dir):
            os.mkdir(model_test_dir)

        init_test_path = os.path.join(model_test_dir, '__init__.py')
        if not os.path.exists(init_test_path) or self.force:
            with open(init_test_path, 'w', encoding='utf8') as f:
                f.write(self.build_init())

        post_test_path = os.path.join(model_test_dir, 'post_test.py')
        if not os.path.exists(post_test_path) or self.force:
            with open(post_test_path, 'w', encoding='utf8') as f:
                f.write(self.build_post())

        delete_test_path = os.path.join(model_test_dir, 'delete_test.py')
        if not os.path.exists(delete_test_path) or self.force:
            with open(delete_test_path, 'w', encoding='utf8') as f:
                f.write(self.build_delete())

        put_test_path = os.path.join(model_test_dir, 'put_test.py')
        if len(self.primary_keys) == 1 and (not os.path.exists(put_test_path) or self.force):
            with open(put_test_path, 'w', encoding='utf8') as f:
                f.write(self.build_put())

        get_test_path = os.path.join(model_test_dir, 'get_test.py')
        if not os.path.exists(get_test_path) or self.force:
            with open(get_test_path, 'w', encoding='utf8') as f:
                f.write(self.build_get())

    def build_init(self):
        template_path = os.path.join(self.dirname, 'templates/test/__prepare__.py')
        with open(template_path, 'r', encoding='utf8') as f:
            template = f.read()
        props = [{'name': k, 'value': v.example} for k, v in self.model.Form.__dict__.items() if isinstance(v, form.Validator)]

        BODY = '\n{}'.format(self.space[12]).join(['"{0}" : "{1}",'.format(item['name'], item['value']) for item in props])

        cols_insert = ', '.join([item['name'] for item in props])
        cols_insert_colon = ':' + ', :'.join([item['name'] for item in props])

        INSERT = 'insert into {0}({1}) values ({2});'.format(self.table.name, cols_insert, cols_insert_colon)

        template = template.replace('[BODY]', BODY).replace('[INSERT]', INSERT)

        return template

    def build_post(self):
        template_path = os.path.join(self.dirname, 'templates/test/post.py')
        with open(template_path, 'r', encoding='utf8') as f:
            template = f.read()


        template = (template
                    .replace('[app_name]', self.app_name)
                    .replace('[model_name]', self.model_name.lower())
                    .replace('[CHECKSQL]', self.CHECKSQL)
                    )

        return template

    def build_delete(self):
        template_path = os.path.join(self.dirname, 'templates/test/delete.py')
        with open(template_path, 'r', encoding='utf8') as f:
            template = f.read()


        template = (template
                    .replace('[app_name]', self.app_name)
                    .replace('[model_name]', self.model_name.lower())
                    .replace('[CHECKSQL]', self.CHECKSQL)
                    )

        return template

    def build_put(self):
        template_path = os.path.join(self.dirname, 'templates/test/put.py')
        with open(template_path, 'r', encoding='utf8') as f:
            template = f.read()


        template = (template
                    .replace('[app_name]', self.app_name)
                    .replace('[model_name]', self.model_name.lower())
                    .replace('[CHECKSQL]', self.CHECKSQL)
                    )

        return template

    def build_get(self):
        template_path = os.path.join(self.dirname, 'templates/test/get.py')
        with open(template_path, 'r', encoding='utf8') as f:
            template = f.read()

        template = (template
                    .replace('[app_name]', self.app_name)
                    .replace('[model_name]', self.model_name.lower())
                    )

        return template


class ControlGen(Gen):
    def __init__(self, model_full_name, force=False, *args, **kwargs):
        super().__init__(model_full_name, force, *args, **kwargs)

        self.build_class()
        self.build_post()
        self.build_delete()
        self.build_update()
        self.build_get()

        ctrl_path = os.path.join(self.app_path, self.app_name, 'controls', self.model_name.lower() + '.py')

        with open(ctrl_path, 'w', encoding='utf8') as f:
            f.write(self.content_class)
            f.write('\n')
            f.write(self.content_post)
            f.write('\n\n')
            f.write(self.content_delete)
            f.write('\n\n')
            f.write(self.content_put)
            f.write('\n\n')
            f.write(self.content_get)

    def build_class(self):
        tempalte_path = os.path.join(self.dirname, 'templates/control/class.py')

        with open(tempalte_path, 'r', encoding='utf8') as f:
            template = f.read()

        template = (template
                    .replace('[module_name]', self.module_name)
                    .replace('[model_name]', self.model_name)
                    )

        self.content_class = template

    def build_post(self):
        tempalte_path = os.path.join(self.dirname, 'templates/control/post.py')

        with open(tempalte_path, 'r', encoding='utf8') as f:
            template = f.read()
        template = template.replace('[model_name]', self.model_name)

        self.content_post = self.indent(template, 4)

    def build_delete(self):
        tempalte_path = os.path.join(self.dirname, 'templates/control/delete.py')

        with open(tempalte_path, 'r', encoding='utf8') as f:
            template = f.read()

        template = (template
                    .replace('[model_name]', self.model_name)
                    .replace('[delete_filter]', self.help_build_filter('GET'))
                    )

        self.content_delete = self.indent(template, 4)

    def build_update(self):
        if len(self.primary_keys) == 1:
            tempalte_path = os.path.join(self.dirname, 'templates/control/put.py')

            with open(tempalte_path, 'r', encoding='utf8') as f:
                template = f.read()

            template = (template
                        .replace('[model_name]', self.model_name)
                        .replace('[pk_filter]', self.help_build_filter('BODY'))
                        )

            self.content_put = self.indent(template, 4)
        else:
            self.content_put = ''

    def build_get(self):
        tempalte_path = os.path.join(self.dirname, 'templates/control/get.py')

        with open(tempalte_path, 'r', encoding='utf8') as f:
            template = f.read()

        template = (template
                    .replace('[model_name]', self.model_name)
                    .replace('[pk_filter]', self.help_build_filter('GET'))
                    )

        self.content_get = self.indent(template, 4)

    @classmethod
    def indent(cls, content, spacecount):
        return cls.space[spacecount] + '\n{0}'.format(cls.space[spacecount]).join(content.splitlines())


class App:
    def __init__(self, app_name):
        # root = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        app_template_path = os.path.join(root, 'generator', 'app')
        app_path = os.path.join(root, app_name)

        if not os.path.exists(app_path):
            # create basic strucuture
            shutil.copytree(app_template_path, app_path)

            # change database name
            init_app = os.path.join(app_path, '__init__.py')

            with open(init_app, 'r', encoding='utf-8') as f:
                c = f.read().replace("dbname", os.path.basename(root))

            with open(init_app, 'w', encoding='utf-8') as f:
                f.writelines(c)


def main(options):
    if options.cmd == 'startapp':
        App(options.app)
    elif options.cmd == 'gen':
        force, model = bool(options.force), options.model
        if not model:
            print('请提供model完整名字(包含模块名)')
        else:
            ControlGen(model, force)
            TestGen(model, force)
