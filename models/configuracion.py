from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder


class Configuracion():
    def __init__(self, id=None, nombre=None, valor=None) -> None:
        self.id = id
        self.nombre = nombre
        self.valor = valor

    def get_configs(self, id):
      # Abrir conexion a la base de datos
        con = db().open
        # Crear un cursor
        cursor = con.cursor()
        # Preparar la consulta
        sql = "select id, nombre, valor from configuracion where id=%s"
        # Ejecutar la consulta sql
        cursor.execute(sql, [id])
        # Capturar los datos que devuelve la consulta sql
        datos = cursor.fetchone()
        # Cerrar el cursor y la conexion a la base de datos
        cursor.close()
        con.close()
        # Retornar resultado
        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'message': 'There aren\'t any registers!'})
