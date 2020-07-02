from fastapi import FastAPI
from fastapi import Depends
from pydantic import BaseModel
from logger3d import D, I, W, E
from matchparam import oparam
import os


app = FastAPI()
teams = os.listdir(oparam['basedir'])
iter_team = iter(teams)


class Feedback(BaseModel):
    result: str


@app.get('/')
def index():
    import socket
    return {'robocup3d': 'welcome',
            'task': 'automatch',
            'master-host': socket.gethostname()}


@app.get('/fullteam')
def fullteam():
    return os.listdir(oparam['basedir'])


@app.get('/onematch')
def onematch():
    global iter_team
    mt = oparam.get('mainteam')
    choose = oparam.get('choose')
    if mt:
        D(f'Main team set to {mt}')
        r = mt
        if choose == 'sequent':
            while r == mt:
                try:
                    r = iter_team.__next__()
                except StopIteration:
                    iter_team = iter(teams)
                    r = iter_team.__next__()
        elif choose == 'random':
            import random
            r = random.choice(list(set(teams)-{mt}))
            I(f'Random choose "{r}"')
        else:
            E(f'Unknown choose type: {choose}')
        return mt+','+r


@app.post('/feedback')
def feed_back(request: Feedback):
    D(f'Receive "{request.result}"')
    with open(oparam['record-fn'], 'a') as f:
        print(request.result, file=f)

    return 'ok'
