import requests
from matchparam import oparam
from logger3d import I, W, E
from auto_match import full_match_with_log
import time


def get_one_task():

    rc = 0
    url = f"http://{oparam['masterHost']}:{oparam['masterPort']}/onematch"
    while rc != 200:
        try:
            r = requests.get(url)
            rc = r.status_code
            if rc != 200:
                W(f'[{rc}] {url}')
                time.sleep(oparam['retrywait'])
        except Exception:
            E(f'Connection Error, retry after {oparam["retrywait"]}s')
            time.sleep(oparam['retrywait'])
            
    t1, t2 = r.text[1:-1].split(',')
    return t1, t2


while True:
    try:
        t1, t2 = get_one_task()
    except KeyboardInterrupt:
        W('Servant catch SIGKIL, exit!')
        break
    full_match_with_log(oparam['basedir']+'/'+t1, oparam['basedir']+'/'+t2)
