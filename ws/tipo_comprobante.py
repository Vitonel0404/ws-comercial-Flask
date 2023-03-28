from flask import Blueprint, request, jsonify
from models.tipo_comprobante import Tipo_Comprobante
import json
import validarToken

ws_tipo_comprobante = Blueprint('ws_tipo_comprobante', __name__)


@ws_tipo_comprobante.route('/tipo_comprobante/venta', methods=['POST'])
@validarToken.validar_token
def catalog():
    if request.method == 'POST':
        obj_tipo = Tipo_Comprobante()
        rpta_json = obj_tipo.list_tipo_comprobante()
        tipo_comprobante_data = json.loads(rpta_json)
        return jsonify(tipo_comprobante_data), 200
