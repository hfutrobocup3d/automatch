import yaml



with open('params.yaml') as f:
    _params = f.read()

optim_params = yaml.safe_load(_params)
oparam = optim_params