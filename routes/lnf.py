import requests
from flask import render_template, Blueprint, Response, request

import config

bp = Blueprint("lnf", __name__)

@bp.route('/css/styles.css', methods=['GET'])
def styles():
    lnf = config.get_lnf(request.host)
    print('host', request.host)
    url = lnf.logo
    css = render_template('css/styles.css', lnf=lnf)
    return Response(css, mimetype='text/css')

@bp.route('/images/logo', methods=['GET'])
def logo():
    lnf = config.get_lnf(request.host)
    url = lnf.logo
    mimetype = 'image/png'
    if url.endswith('.jpg'):
        mimetype = 'image/jpeg'
    return Response(requests.get(url).content, mimetype=mimetype)