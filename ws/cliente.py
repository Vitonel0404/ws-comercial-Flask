from flask import Blueprint, request, jsonify
from models.cliente import Cliente
import json
import validarToken

ws_cliente =Blueprint('ws_cliente',__name__)

@ws_cliente.route('/cliente/catalogo',methods=['POST'])
@validarToken.validar_token
def catalogo_cliente():
    if request.method == 'POST':
        objCliente = Cliente()
        rptaJSON = objCliente.listaCliente()
        datos_cliente = json.loads(rptaJSON)
        return jsonify(datos_cliente),200
