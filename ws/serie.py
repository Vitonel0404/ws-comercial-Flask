from flask import Blueprint, request, jsonify
from models.serie import Serie
import json
import validarToken

ws_serie = Blueprint('ws_serie', __name__)


@ws_serie.route('/serie/venta', methods=['POST'])
@validarToken.validar_token
def catalog():
    if request.method == 'POST':
        tc_id = request.form['tc_id']
        obj_serie = Serie()
        rpta_json = obj_serie.list_serie(tc_id)
        serie_data = json.loads(rpta_json)
        return jsonify(serie_data), 200
