import yaml




_params = '''
basedir: /home/shan/2019
mainteam: HFUTEngine

masterHost: 192.168.2.194:8000


# choose: [sequent, random]
choose: sequent
record-fn: output.txt
'''


optim_params = yaml.safe_load(_params)
oparam = optim_params