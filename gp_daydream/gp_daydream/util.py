# -*- encoding:utf-8 -*-
import time
def value_strip(value):
    if isinstance(value, unicode):
        return value.strip()
    else:
        return value.strip().decode('utf8')

def get_date():
    now = int(time.time())
    timeArray = time.localtime(now)
    return value_strip(time.strftime("%Y-%m-%d", timeArray))