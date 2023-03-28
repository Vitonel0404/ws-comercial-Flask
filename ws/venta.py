from re import VERBOSE
from flask import Blueprint, request, jsonify
from models.venta import Venta
import json
import validarToken

ws_venta =Blueprint('ws_venta',__name__)
@ws_venta.route('/venta/insertar',methods=['POST'])
@validarToken.validar_token
def insertar_venta():
    if request.method=='POST':
        #recibir datos de los parametros
        cliente_id=request.form['cliente_id']
        tipo_comprobante_id=request.form['tipo_comprobante_id']
        nser=request.form['nser']
        ndoc=0
        fdoc=request.form['fdoc']
        sub_total=request.form['sub_total']
        igv=request.form['igv']
        total=request.form['total']
        porcentaje_igv=request.form['porcentaje_igv']
        usuario_id_registro=request.form['usuario_id_registro']
        almacen_id=request.form['almacen_id']
        detalle_venta=request.form['detalle_venta']

        objVenta=Venta(cliente_id,tipo_comprobante_id,nser,ndoc,fdoc,sub_total,igv,total,porcentaje_igv,usuario_id_registro,almacen_id,detalle_venta)
        rptaJSON= objVenta.insertar()
        datos_venta=json.loads(rptaJSON)

        #imprimir resultados
        return jsonify(datos_venta),200 #200 -> Ok
