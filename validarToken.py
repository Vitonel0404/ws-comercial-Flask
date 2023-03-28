###########################################
#este archivo valida el token y otorgará o
#denegará al servicio web segun sea el caso
###########################################

from flask import jsonify, request
import jwt
from functools import wraps
from config import SecretKey
import json
from models.sesion import Sesion

#validar el estado del token del usuario
def validar_estado_token_usuario(usuario_id):
    objSesion = Sesion()
    rptaJSON = objSesion.validarEstadoToken(usuario_id)
    datos_token=json.loads(rptaJSON)
    if datos_token['status'] == True: ##significa que he devuelto el estado del token
        estado_token_usuario= datos_token['data']['estado_token']
        if estado_token_usuario == None:
            return False#el usuario no tendra acceso al servicio web
        else:
            if estado_token_usuario == '0': #El token esta inactivo
                return False#el usuario no tendra accesoal servicio web
            else:
                return True# es usuario si tendra acceso al servicio web
    else:
        return False # el usuario  no tendra acceso al servicio web

def validar_token(fx):
    @wraps(fx)
    def decorated(*args, **kwargs):
        token =request.form['token']

        if not token:
            return jsonify({'status':False, 'data':'No hay datos'}), 403
        try:
            #decodificar el token
            data = jwt.decode(token, SecretKey.JWT_SECRET_KEY, algorithms="HS256")
            #data = jwt.decode(token, SecretKey.JWT_SECRET_KEY)
            #extraer el id del usuario
            usuario_id=data['usuario_id']
            #consultar el estadodel token
            estado_token=validar_estado_token_usuario(usuario_id)

            if estado_token == False:
                return jsonify({'status':False, 'data':'El token se encuentra inactivo'}), 403
        except (jwt.DecodeError, jwt.ExpiredSignatureError) as error:
            return jsonify({'status':False, 'data':'El token es inválido','internal token error':format(error)}), 403
        except (Exception) as error:
            return jsonify({'status':False, 'data':format(error)}), 403
        
        return fx(*args, **kwargs)

    return decorated

