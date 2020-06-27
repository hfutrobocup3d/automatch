#!/usr/bin/env python3
import subprocess


# Path like this
roboviz_path = '/home/wistral/RoboViz-dev/bin/linux-amd64/roboviz.sh'

def start_roboviz(serverHost='localhost', serverPort=3200):
    return subprocess.Popen([
        roboviz_path,
        f'--serverHost={serverHost}',
        f'--serverPort={serverPort}'
    ])
    
    
if __name__ == '__main__':
    #start_roboviz()
    start_roboviz('192.168.1.113')

