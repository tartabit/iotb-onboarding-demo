import yaml
from dataclasses import dataclass
from typing import List

@dataclass
class Iotb:
    url: str
    api_suffix: str
    token: str
    debug: bool

@dataclass
class Protocol:
    name: str
    solution: str

@dataclass
class Target:
    name: str
    solution: str

@dataclass
class Onboarding:
    parentAccountId: str

@dataclass
class Config:
    iotb: Iotb
    protocols: List[Protocol]
    targets: List[Target]
    onboarding: Onboarding

iotb: Iotb
protocols: List[Protocol]
targets: List[Target]
onboarding: Onboarding

def load_config(file_path: str) -> Config:
    global config, iotb, protocols, targets, onboarding

    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    iotb = Iotb(**config_data['iotb'])
    protocols = [Protocol(**protocol) for protocol in config_data['templates']['protocol']]
    targets = [Target(**target) for target in config_data['templates']['target']]
    onboarding = Onboarding(**config_data['onboarding'])

    config = Config(iotb=iotb, protocols=protocols, targets=targets, onboarding=onboarding)
    return config
