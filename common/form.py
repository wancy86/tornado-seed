import re
import sys
from datetime import datetime
import time
import common


class Form:
    def __init__(self, **kwargs):
        self.data = {}
        for k, v in type(self).__dict__.items():
            if isinstance(v, Validator):
                # 如果验证失败，此方法会跑出异常
                setattr(self, k,
                        {
                            'name': v.name,
                            'val': kwargs.get(k),
                            'message': v.message
                        }
                        )

                self.data[k] = kwargs.get(k)
        if kwargs.get('entry_user'):
            self.data['entry_user'] = kwargs.get('entry_user')

    @classmethod
    def json(cls):
        config = {}
        for k, v in cls.__dict__.items():
            if isinstance(v, Validator):
                config[k] = v.__dict__

        return config


class InvalidException(Exception):

    __slots__ = ('name', 'value', 'message')

    def __init__(self, name, value, message):
        self.name = name
        self.value = value
        self.message = message

    def __str__(self):
        return '{}({}){}'.format(self.name, self.value if self.value else '空值', self.message)


class Validator:

    def __init__(self, name, nullable, message=None, example=None, **kwargs):
        self.name = name
        self.nullable = nullable
        self.message = message if message else '验证通不过！'
        self.example = example

    def __set__(self, instance, value):
        if not self(value):
            raise InvalidException(value['name'], value['val'], value['message'])


class List(Validator):

    def __init__(self, name, nullable=False, message=None, example=None, minlength=0, maxlength=9999, **kwargs):
        message = '不符合规则(数组且长度为{}-{})'.format(str(minlength), maxlength)
        super().__init__(name, nullable, message, example, **kwargs)
        self.minlength = minlength
        self.maxlength = maxlength

    def __call__(self, value):
        if not value['val']:
            return self.nullable
        else:
            val = value['val']
            if isinstance(val, list):
                length = len(val)
                if (self.minlength and length < self.minlength) or (self.maxlength and length > self.maxlength):
                    return False
                else:
                    return True
            return False


class String(Validator):

    def __init__(self, name, nullable=False, message=None, example=None, minlength=None, maxlength=None, pattern=None, **kwargs):
        super().__init__(name, nullable, message, example, **kwargs)
        self.minlength = minlength
        self.maxlength = maxlength
        self.pattern = pattern

    def __call__(self, value):
        if not value['val']:
            return self.nullable
        else:
            val = str(value['val'])
            length = len(val)

            if (self.minlength and length < self.minlength) or \
               (self.maxlength and length > self.maxlength) or \
               (self.pattern and not re.compile(self.pattern).search(val)):
                return False

            return True


class Integer(Validator):

    def __init__(self, name, nullable=False, message=None, example=None, minvalue=None, maxvalue=None, **kwargs):
        super().__init__(name, nullable, message, example, **kwargs)
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def __call__(self, value):
        if value['val'] == None:
            return self.nullable
        else:
            try:
                val = int(value['val'])
                if (self.minvalue and val < self.minvalue) or (self.maxvalue and val > self.maxvalue):
                    return False
                else:
                    return True
            except Exception as e:
                return False


# class Date(Validator):

#     def __init__(self, name, nullable=False, message=None, example=None, minlength=None, maxlength=None, pattern='%Y-%m-%d', **kwargs):
#         super().__init__(name, nullable, message, example, **kwargs)
#         self.pattern = pattern
#         self.minlength = datetime.strptime(minlength, self.pattern)
#         self.maxlength = datetime.strptime(maxlength, self.pattern)

#     def __call__(self, value):
#         if value['val'] == None:
#             return self.nullable or value['nullable']
#         else:
#             val = datetime.strptime(value['val'], self.pattern)
#             if (self.minlength and val < self.minlength) or \
#                (self.maxlength and val > self.maxlength):
#                 return False
#             return True


# class Datetime(Date):
#     pattern = '%Y-%m-%d %H:%M:%S'

#     def __init__(self, name, nullable=False, message=None, example=None, minlength=None, maxlength=None, **kwargs):
#         super().__init__(name, nullable, message=message, example=example, minlength=minlength, maxlength=maxlength, pattern=self.pattern, **kwargs)


class Email(String):

    pattern = r"^[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$"

    def __init__(self, name, nullable=False, message="不符合邮箱格式", example=None, **kwargs):
        super().__init__(name, nullable, message=message, example=example, pattern=self.pattern, **kwargs)


class Mobile(String):

    pattern = r"^(1|861|\+861|0861|\+0861)\d{10}$"

    def __init__(self, name, nullable=False, example=None, **kwargs):
        super().__init__(name, nullable, example=example, pattern=self.pattern, **kwargs)
