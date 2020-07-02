import requests
from matchparam import oparam
from logger3d import I, W
from auto_match import full_match_with_log
import time


def get_one_task():

    rc = 0
    url = 'http://'+oparam['masterHost']+'/onematch'
    while rc != 200:
        r = requests.get(url)
        rc = r.status_code
        if rc != 200:
            W(f'[{rc}] {url}')
            time.sleep(20)
    t1, t2 = r.text[1:-1].split(',')
    return t1, t2


while True:
    t1, t2 = get_one_task()
    full_match_with_log(oparam['basedir']+'/'+t1, oparam['basedir']+'/'+t2)
