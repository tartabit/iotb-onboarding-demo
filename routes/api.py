import json

from flask import Blueprint, request, jsonify
import config
import iotb

bp = Blueprint("api", __name__)

@bp.route('/api/onboard', methods=['POST'])
def onboard():
    account_id = request.form.get('account')
    new_account_name = request.form.get('new_account_name')
    protocol = request.form.get('protocol')
    target = request.form.get('target')
    source_cidr = request.form.get('source_cidr')

    print(request.form)

    results = []

    selected_proto = None
    for proto in config.protocols:
        if protocol == proto.name:
            selected_proto = proto
            break

    selected_target = None
    for targ in config.targets:
        if target == targ.name:
            selected_target = targ
            break

    if not selected_proto or not selected_target:
        return "Invalid protocol or target", 500

    proto_solution = iotb.get_solution(selected_proto.solution)
    proto_solution['template'] = {}
    proto_solution['startTriggers'] = True
    del proto_solution['templateDef']
    for field in request.form:
        if field.startswith("protodef-"):
            field_name = field[9:]
            proto_solution['template'][field_name]=request.form.get(field)

    target_solution = iotb.get_solution(selected_target.solution)
    target_solution['template'] = {}
    target_solution['startTriggers'] = True
    del target_solution['templateDef']
    for field in request.form:
        if field.startswith("targetdef-"):
            field_name = field[10:]
            target_solution['template'][field_name]=request.form.get(field)


    # 1. ACCOUNT
    account = None
    if new_account_name:
        # create a new account as a child of the onboarding parent account.
        result = iotb.client.request('POST', 'account', body={'name': new_account_name},
                                         account_id=config.onboarding.parentAccountId)
        if result.status == 201:
            account = result.body
            account_id = account['id']
            results.append(f"Created account [{account['name']}] with ID: {account_id}")
    else:
        # lookup an existing account.
        account = iotb.client.request('GET', 'account/'+account_id, account_id=config.onboarding.parentAccountId).body
        results.append(f"Found account [{account['name']}] with ID: {account_id}")

    # 2. DEFINE PROTOCOL HANDLER
    protocol_result = iotb.client.request('POST', 'import', body=proto_solution, account_id=account_id)
    if protocol_result.status == 200:
        results.append(f"Created protocol handler.")
    else:
        results.append(f"Failed to create protocol handler: {protocol_result.status} - {protocol_result.body}")

    # 3. DEFINE TARGET
    target_result = iotb.client.request('POST', 'import', body=target_solution, account_id=account_id)
    if target_result.status == 200:
        results.append(f"Created target handler.")
    else:
        results.append(f"Failed to create target handler: {target_result.status} - {target_result.body}")

    # Here you can add the functionality to execute the operations
    # For now, we will just return the received data as a JSON response
    response_data = {
        'results': results,
        'account': account,
        'protocolTemplate': proto_solution,
        'protocolResult': protocol_result.to_dict(),
        'targetTemplate': target_solution,
        'targetResult': target_result.to_dict(),
        'source_cidr': source_cidr
    }
    pretty_response = json.dumps(response_data, indent=4)
    return pretty_response, 200, {'Content-Type': 'application/json'}