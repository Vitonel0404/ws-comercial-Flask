#importar los paquetes necesarios para implementar la web services
import json
from flask import Blueprint, request, jsonify
from werkzeug.utils import validate_arguments
from models.producto import Producto
from config import SecretKey
import jwt
import datetime
import validarToken
ws_producto=Blueprint('ws_producto',__name__)

@ws_producto.route('/producto/catalogo',methods=['POST'])
@validarToken.validar_token #Funcion que permite validar 
def catalogo():
    if request.method== 'POST':
        id_almacen=request.form['id_almacen']
        objProductos = Producto()
        rptJSON= objProductos.listarProductosCatalogos(id_almacen)
        datos_productos = json.loads(rptJSON)
        return jsonify(datos_productos), 200

