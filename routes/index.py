import requests
from flask import Blueprint, render_template, abort
import config
import iotb

bp = Blueprint("index", __name__)

@bp.route('/')
def index():
    accounts = iotb.client.request('GET', 'account', {'userScope': True}, account_id=config.onboarding.parentAccountId).body
    return render_template('index.html', accounts=accounts)
