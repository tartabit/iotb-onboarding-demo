import requests
from flask import Blueprint, render_template, abort
import config
import iotb

bp = Blueprint("onboarding", __name__)

@bp.route('/onboarding')
def onboarding():
    accounts = iotb.client.request('GET', 'account', {'userScope': True}, account_id=config.onboarding.parentAccountId).body
    accounts  = [account for account in accounts if account['id'] != config.onboarding.parentAccountId]

    protocols = []
    for proto in config.protocols:
        sln = iotb.get_solution(proto.solution)
        if sln:
            protocols.append({"name": proto.name, "def": sln['templateDef']})

    targets = []
    for target in config.targets:
        sln = iotb.get_solution(target.solution)
        if sln:
            targets.append({"name": target.name, "def": sln['templateDef']})

    return render_template('onboarding.html', accounts=accounts, protocols=protocols, targets=targets)
