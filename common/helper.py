from datetime import datetime

def format_datetime(value):
    return '{}-{}-{} {}:{}'.format(value.year, value.month, value.day, value.hour, value.minute)