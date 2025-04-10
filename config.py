import yaml
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Iotb:
    url: str
    api_suffix: str
    token: str
    debug: bool
    insecure: bool

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
class LookAndFeel:
    logo: str
    colors: Dict[str, str]

@dataclass
class Config:
    iotb: Iotb
    protocols: List[Protocol]
    targets: List[Target]
    onboarding: Onboarding
    lnf: Dict[str, LookAndFeel]

iotb: Iotb
protocols: List[Protocol]
targets: List[Target]
onboarding: Onboarding
lnf: Dict[str, LookAndFeel]

def load_config(file_path: str) -> Config:
    global config, iotb, protocols, targets, onboarding, lnf

    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    iotb = Iotb(**config_data['iotb'])
    protocols = [Protocol(**protocol) for protocol in config_data['templates']['protocol']]
    targets = [Target(**target) for target in config_data['templates']['target']]
    onboarding = Onboarding(**config_data['onboarding'])
    lnf = {key: LookAndFeel(**value) for key, value in config_data['lnf'].items()}

    config = Config(iotb=iotb, protocols=protocols, targets=targets, onboarding=onboarding, lnf=lnf)
    return config

def get_lnf(host: str) -> LookAndFeel:
    return config.lnf.get(host, config.lnf.get('default'))
