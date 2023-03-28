from flask import Blueprint, request, jsonify
from models.configuracion import Configuracion
import json
import validarToken

ws_configuracion = Blueprint('ws_configuracion', __name__)


@ws_configuracion.route('/config', methods=['GET'])
@validarToken.validar_token
def catalog():
    if request.method == 'GET':
        id = request.form['id']
        obj_conf = Configuracion()
        rpta_json = obj_conf.get_configs(id)
        config_data = json.loads(rpta_json)
        return jsonify(config_data), 200
