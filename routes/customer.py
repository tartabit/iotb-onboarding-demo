import logging
import math
import json

import requests
from flask import Blueprint, render_template, abort, request
import config
import iotb

bp = Blueprint("customer", __name__)

def truncate_float(value, decimals):
    factor = 10 ** decimals
    return math.trunc(value * factor) / factor

@bp.route('/customer/<account_id>', methods=['GET'])
def customer(account_id):
    if not account_id:
        return "Account ID is required", 400

    acct = iotb.client.request('GET', 'account/$self', account_id=account_id).body

    services = iotb.client.request('GET', 'service', account_id=account_id).body
    service_statuses = iotb.client.request('GET', 'metrics/status', {'object': 'services', 'pivot': 'serviceId'}, account_id=account_id).body

    logs = iotb.client.request('GET', 'log', {'limit': 100}, account_id=account_id).body
    events = iotb.client.request('GET', 'events',{'query': 'type==generic && data.key==data', 'limit': 100 }, account_id=account_id).body

    for service in services:
        if service['id'] not in service_statuses['results']:
            continue
        status = service_statuses['results'][service['id']]
        del status['entry']
        logging.info(f"status {status}")
        if status:
            for period_name, period in status.items():
                logging.info(f"period {period}")
                if period['count'] > 0:
                    period['pct'] = str(truncate_float(float(period['success']) / float(period['count']) * 100, 1)) + '%'
                else:
                    period['pct'] = '-'
            service['metrics'] = status
        else:
            service['metrics'] = {}

    return render_template('customer.html', account=acct, services=services, logs=logs, events=events)
