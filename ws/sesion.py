##################################
# Este sericio web permitirá al usuario inicir sesión Y
# generar su token de seguridad utilizando JWT
##################################

#importar los paquetes necesarios para implementar la web services
import json
from flask import Blueprint, request, jsonify
from models.sesion import Sesion
from config import SecretKey
import jwt
import datetime

ws_sesion = Blueprint('ws_sesion',__name__) #opera como un módulo donde se implementará el o la web services de inicio de sesión
@ws_sesion.route('/login',methods=['POST'])
def auth():
    if request.method == 'POST':
        #recoger los datos que vienen por post y que permite iniciar sesion
        email =request.form['email']
        clave =request.form['clave']
        # instanciar el objeto de clase sesion para enviar el email y la clave
        objSesion = Sesion(email,clave)
        rptaJSON=objSesion.iniciar_sesion()
        datos_sesion = json.loads(rptaJSON) #convertir una cadena JSON a objeto
        if datos_sesion['status']==True:
            usuario_id = datos_sesion['data']['id']
            #generar el token del usuario con JWT
            token=jwt.encode({'usuario_id':usuario_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=24)}, SecretKey.JWT_SECRET_KEY)
            ############ actualizar el token
            objSesion.actualizarToken(token, usuario_id)
            #agregar al token al inicio de sesion
            datos_sesion['data']['token']=token
            #generar la URL donde está almacenada la foto del usuario
            datos_sesion['data']['img'] ='/static/imgs/'+ datos_sesion['data']['img']
            #retornar resultado en formato JSON
            return jsonify(datos_sesion),200 #Status WS -> OK
        else:
            return jsonify(datos_sesion),401 # -> el usuario no está autorizado a ingresar
