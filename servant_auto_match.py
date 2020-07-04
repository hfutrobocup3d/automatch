import requests
from matchparam import oparam
from logger3d import I, W, E
from auto_match import full_match_with_log
import time
import os


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
    
    try:
        base_dir = os.environ['SRC_FOLDER']
        I(f'Found ENV ARG SRC_FOLDER={base_dir}')
    except KeyError:
        base_dir = oparam['basedir']
        I(f'Not Found ENV ARG SRC_FOLDER, set to {base_dir}')

    r = full_match_with_log(base_dir+'/'+t1, base_dir+'/'+t2)
    if r:
        with open(oparam['record-fn'], 'a') as f:
            print(r, file=f)
        I(f'')
    else:
        E('Match error!')
        os._exit(1)
