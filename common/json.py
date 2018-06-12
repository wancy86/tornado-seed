from datetime import datetime, date

''' result:sqlalchemy.engine.result.ResultProxy'''
def json_by_result(result):
    data = []
    for row in result:
        record = {}
        for item in row.items():
            record[item[0]] = str(item[1]) if item[1] or item[1] == 0 else ''
        data.append(record)    
    return data


def plus(*args):
    data = {}
    for d in args:
        for key, value in d.items():
            data[key] = value
    return data

def j(instance):
    '''convert the instance to dictionary'''
    data = {}
    for p in dir(instance):
        if p.startswith('__') and p.endswith('__'):
            continue
        else:
            data[p] = getattr(instance, p)
    return data


def jj(*args):
    '''join the two dictionary, this method is deprecated, please us plus to replace this one'''
    data = {}
    for d in args:
        for key, value in d.items():
            data[key] = value
    return data


def dict_select(dict_obj, *args):
    data = {}
    if isinstance(dict_obj, dict):
        for arg in args:
            data[arg] = dict_obj[arg]
    return data


def dict_unselect(dict_obj, *args):

    if isinstance(dict_obj, dict):
        return_obj = dict_obj.copy()
        for arg in args:
            return_obj.pop(arg, '')
    return return_obj


def dict_json(dict_obj):
    data = {}
    if isinstance(dict_obj, dict):
        for key, value in dict_obj.items():
            if isinstance(value, datetime):
                data[key] = '{}-{}-{} {}:{}'.format(
                    value.year, value.month, value.day, value.hour, value.minute)
            elif isinstance(value, date):
                data[key] = '{}-{}-{}'.format(
                    value.year, value.month, value.day)
            else:
                data[key] = str(value)
    return data
