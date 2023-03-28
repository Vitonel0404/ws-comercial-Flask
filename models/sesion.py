
from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder
class Sesion():
    def __init__(self, p_email=None, p_clave=None):
        self.email = p_email
        self.clave= p_clave
    
    def iniciar_sesion(self):
        #abrir la conexion
        con = db().open

        #crear un cursor
        cursor =con.cursor()

        #Preparar la consulta SQL para validar las credenciales del usuario
        sql="select id, nombre, email, img, estado_usuario, almacen_id from usuario where email=%s and clave=%s"
        #ejecutar la consulta SQL 
        cursor.execute(sql,[self.email,self.clave])

        #capturar los datos que devuelve la consulta sql mediante al cursor
        datos= cursor.fetchone()

        #Cerrar la conexion y el cursor a la bd
        cursor.close()
        con.close()
        if datos: #si el cursor trae datos
            if datos['estado_usuario']=='1':#si el usuario está activo
                return json.dumps({'status':True,'data':datos})
            else:
                return json.dumps({'status':False, 'data': 'El usuario se encuentra inactivo, consulte con el administrador del sistema'})
        else:
            return json.dumps({'data': 'Usuario o contraseña incorrectos'})

    def actualizarToken(self, token, id):
        con = db().open

        #indicar a python que los cambios se harán de manera manual
        con.autocommit = False
        cursor =con.cursor()
        sql= "update usuario set token=%s, estado_token='1' where id=%s"
        try:
            #ejecutar la sentencia sql
            cursor.execute(sql,[token,id])
            #confirmar la actualizacion
            con.commit()

            #retornar un mensaje 
            return json.dumps({'status':True, 'data':'Token actualizado'})
        except con.Error as error:
            #Revocar los cambios realizados en la conexion
            con.rollBack()
            #retornar un mensajito de error
            return json.dumps({'status':False, 'data':format(error)},cls=CustomJsonEncoder)
        finally:
            cursor.close()
            con.close()
    
    def validarEstadoToken(self, usuario_id):
        con=db().open
        cursor=con.cursor()
        sql="select estado_token from usuario where id=%s"
        cursor.execute(sql,[usuario_id])
        datos = cursor.fetchone()
        cursor.close()
        con.close()
        if datos:
            return json.dumps({'status':True, 'data':datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status':False, 'data':'No hay datos'})