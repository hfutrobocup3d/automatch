#!/usr/bin/env python3
import subprocess
import os
import time
import shutil
import uuid
from logparse import getInfo
from kickoff import kickoff, kickoff_penalty
import datetime


def folder_to_team(fn):
    '''correct team names which diff from folder name'''
    base = {}
    return base.get(fn, fn.split('/')[-1])


def start_server(kwargs=None):
    if kwargs:
        cmd = [f'{k}={v}' for k, v in kwargs.items()]
        cmd = ['rcssserver3d', *cmd]
    else:
        cmd = ['rcssserver3d']
    print(f'execute `{" ".join(cmd)}`')
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def log_mode_server(rb='./rcssserver3d.rb'):
    return start_server({'--script-path': rb})


class NaoAgents:
    def __init__(self, agent_dir, serverHost='127.0.0.1'):
        self.dir = agent_dir
        self.serverHost = serverHost

    def start(self):
        time.sleep(1)
        proc = subprocess.Popen(
            ['bash', 'start.sh', self.serverHost], cwd=self.dir, universal_newlines=True, bufsize=0
        )
        t = 0
        '''poll函数返回码：
            0 正常结束
            1 sleep
            2 子进程不存在
            -15 kill
            None 在运行'''
        while proc.poll() is None:
            time.sleep(1)
            t += 1
        print(f'wait for {t} seconds')
        return proc

    def start_penalty_kick(self):
        time.sleep(1)
        return subprocess.Popen(f'./start_penalty_kicker.sh', cwd=self.dir, stdout=subprocess.PIPE)

    def start_penalty_goalie(self):
        time.sleep(1)
        return subprocess.Popen(f'./start_penalty_goalie.sh', cwd=self.dir, stdout=subprocess.PIPE)

    def kill(self):
        time.sleep(1)
        return subprocess.Popen(f'./kill.sh', cwd=self.dir, stdout=subprocess.PIPE)


def start_half_match(t1_dir, t2_dir, server_started=True, log=True, log_rn='', last_t=300):
    log_fn = 'sparkmonitor.log'
    if log_fn in os.listdir('.'):
        os.remove(log_fn)
    if not server_started:
        server = log_mode_server() if log else start_server()
    left = NaoAgents(t1_dir)
    right = NaoAgents(t2_dir)
    try:
        left.start()
        time.sleep(1)
        right.start()
        time.sleep(1)
        kickoff()
        c = 0
        while True:
            time.sleep(1)
            info = getInfo(log_fn)
            if info is None:
                c += 1
                continue
            else:
                c = 0
            if c > 10:
                print(f'error with logFile!')
                break
            assert type(info) is dict, f'type of info is {type(info)}'
            if int(float(info.get('time', 0))) >= last_t:
                break
    except KeyboardInterrupt:
        return
    finally:
        left.kill()
        right.kill()
        if not server_started:
            server.kill()

        if log and log_rn:
            shutil.move(log_fn, 'log/'+log_rn)
        else:
            os.remove(log_fn)

    if info:
        return info['score']


def start_penalty():
    pass


def full_match_with_log(t1_dir, t2_dir, penalty=True):
    t1name, t2name = t1_dir.split("/")[-1], t2_dir.split("/")[-1]
    ts = str(datetime.datetime.now())[:-7]
    rst1 = start_half_match(t1_dir, t2_dir, log=True, server_started=False,
                            log_rn=f'{t1name}-VS-{t2name}-{ts}-firstHalf.log'
                            )
    if rst1 is None:
        return
    rst2 = start_half_match(t2_dir, t1_dir, log=True, server_started=False,
                            log_rn=f'{t2name}-VS-{t1name}-{ts}-secondHalf.log'
                            )
    if rst2 is None:
        return
    t1score, t2score = rst1[0]+rst2[1], rst1[1]+rst2[0]

    return ','.join([ts, t1name, t2name, str(t1score), str(t2score)])


def cross_full_match():
    teams = 'BahiaRT FCPortugal HFUTEngine ITAndroids magmaOffenburg UTAustinVilla WrightOcean'.split()
    base = '/home/shan/2019/'
    for i, a in enumerate(teams):
        for b in teams[i:]:
            if a == b:
                continue
            r = full_match_with_log(base+a, base+b)
            if r:
                with open('output-cross.txt', 'a') as f:
                    print(r, file=f)
            else:
                print('Match error!')
                os._exit(1)


def us_full_match():
    teams = 'BahiaRT FCPortugal ITAndroids magmaOffenburg UTAustinVilla WrightOcean'.split()
    base = '/home/shan/2019/'
    a = 'HFUTEngine'
    for i, b in enumerate(teams):
        r = full_match_with_log(base+a, base+b)
        if r:
            with open('output-us.txt', 'a') as f:
                print(r, file=f)
        else:
            print('Match error!')
            os._exit(1)


if __name__ == "__main__":
    us_full_match()