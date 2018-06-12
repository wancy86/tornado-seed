import tornado.ioloop as ioloop

from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line
from tornado.web import RequestHandler
from tornado import httpserver

import sys
import os
import re
import shutil
import unittest
import time
from datetime import datetime
import urls
import types

from common.form import Form
import config as conf
from importlib import import_module as im
import common
import multiprocessing
import unittest
import json
import ssl

MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB


def run(port, test=0, https=0):
    conf.TEST = test
    app = urls.get_application()
    if https == '1':
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(conf.HTTPS_CRT_PATH, conf.HTTPS_KEY_PATH)
        server = httpserver.HTTPServer(app, max_buffer_size=GB, ssl_options=ssl_ctx)
        print('https enable')
    else:
        server = httpserver.HTTPServer(app, max_buffer_size=GB)

    if not test:
        print('SERVICE START, PORT:', port)
    server.listen(port)
    ioloop.IOLoop.current().start()


def test(start_dir, pattern='*test.py'):
    try:
        suite = unittest.TestLoader().discover(start_dir, pattern=pattern, top_level_dir=".")

        unittest.TextTestRunner(verbosity=2).run(suite)
    except Exception as e:
        print(e)


def migrate(mode=0):
    regex = re.compile('^[0-9]{4}\.sql$')
    for app in conf.INSTALLED_APPS:
        module = im(app)

        database = conf.DATABASES[module.database][mode]
        conn = common.db.DB(**database)

        # 无条件运行 0000.sql
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), app, 'migrations')

        cmd = "mysql -h{0} -u{1} -p{2} {3} < {4}".format(conn.host, conn.user, conn.password, conn.database,
                                                         os.path.join(path, '0000.sql'))
        cmd += ' 2>&1 | grep -v "Warning: Using a password" '
        os.system(cmd)

        # 检查所有的以四个数字命名的文件，如果没有运行过，则运行，并更新版本库
        files = os.listdir(path)
        files.sort()
        for file in files:
            if regex.match(file) and file != '0000.sql':
                sql = "select app, version from migration where app = '{0}' and version = '{1}';".format(app, file[0:4])
                result = conn.session.execute(sql)
                if not result.first():
                    cmd_sql = "insert into migration (app, version) values ('{0}', '{1}');".format(app, file[0:4])
                    conn.session.execute(cmd_sql)
                    conn.session.commit()
                    cmd_migrate = "mysql -h{0} -u{1} -p{2} {3} < {4}".format(conn.host, conn.user, conn.password,
                                                                             conn.database, os.path.join(path, file))
                    cmd_migrate += ' 2>&1 | grep -v "Warning: Using a password" '
                    print(conn.database, os.path.join(path, file))
                    os.system(cmd_migrate)
        conn.close()


def clear_database(test=0, app_name='all'):
    for app in conf.INSTALLED_APPS:
        # 执行cls.sql
        if app == app_name or app_name == 'all':
            module = im(app)
            conn = common.db.DB(**conf.DATABASES[module.database][test])
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), app, 'migrations')
            clear_cmd = "mysql -h{0} -u{1} -p{2} {3} < {4}".format(conn.host, conn.user, conn.password, conn.database,
                                                                   os.path.join(path, 'cls.sql'))
            clear_cmd += ' 2>&1 | grep -v "Warning: Using a password" '
            os.system(clear_cmd)


def parse_direction(path):
    if path == 'all':
        return {'start_dir': '.'}
    else:
        result = re.match(r'(.*)((?<=\\).*.py)$', path)
        if result != None:
            return {'start_dir': result.group(1), 'pattern': result.group(2)}
        else:
            return {'start_dir': path}


def make_validation_json(app_name='all'):
    for app in conf.INSTALLED_APPS:
        if (app == app_name) or app_name == 'all':
            validation = {}
            for form in Form.__subclasses__():
                if form.__module__.split('.')[0] == app:
                    # 如果类的全路径里面是在对应的application里面
                    k, v = form.json()
                    validation[k] = v
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'validator', app)
            file_name = os.path.join(path, 'validator.json')
            with open(file_name, 'w') as file:
                json.dump(validation, file, ensure_ascii=False, indent=2)


def main():
    if options.cmd == 'runserver':
        run(options.port, 0, options.https)
    elif options.cmd == 'test':
        migrate(1)
        clear_database(test=1)
        process_server = multiprocessing.Process(target=run, kwargs={'port': conf.TEST_PORT, 'test': 1})
        process_test = multiprocessing.Process(target=test, kwargs=parse_direction(options.app))
        process_server.start()
        process_test.start()

        while True:
            try:
                if not process_test.is_alive():
                    process_server.terminate()
                    break
                time.sleep(1)
            except Exception as e:
                process_server.terminate()
                process_test.terminate()

    elif options.cmd == 'migrate':
        migrate(0)

    elif options.cmd == 'makevalidation':
        make_validation_json(options.app)


if __name__ == '__main__':

    define("cmd", default="runserver", help="runserver|startapp|test|migrate|makevalidation", type=str)

    define("app", default="appname|all(only for test)", help="apps", type=str)
    define("port", default=9000, help="service port", type=int)

    define("model", default="", help="the full name of the model", type=str)
    define("force", default="", help="override the current file or not", type=str)

    define("https", default="", help="enable https,set '1' for enable", type=str)

    parse_command_line()

    main()

    try:
        from generator import gen

        gen.main(options)
    except ImportError as e:
        pass
        # print(e.msg)
