import requests

import config
from pyiotb import IotbClient

client: IotbClient

def get_solution(solution: str):
    response = requests.get(config.iotb.url + '/solutions/' + solution, verify=not config.iotb.insecure)
    if response.status_code == 404:
        return None
    data = response.json()
    return data

def configure():
    global client
    client = IotbClient(
        url=config.iotb.url + config.iotb.api_suffix,
        token=config.iotb.token,
        debug=config.iotb.debug,
        insecure=config.iotb.insecure)