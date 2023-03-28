from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder


class Tipo_Comprobante():
    def __init__(self, id=None, tipo_sunat=None, nombre=None) -> None:
        self.id = id
        self.tipo_sunat = tipo_sunat
        self.nombre = nombre

    def list_tipo_comprobante(self):
      # Abrir conexion a la base de datos
        con = db().open
        # Crear un cursor
        cursor = con.cursor()
        # Preparar la consulta
        sql = "select id, tipo_sunat, nombre from tipo_comprobante WHERE venta = 1 order by nombre"
        # Ejecutar la consulta sql
        cursor.execute(sql)
        # Capturar los datos que devuelve la consulta sql
        datos = cursor.fetchall()
        # Cerrar el cursor y la conexion a la base de datos
        cursor.close()
        con.close()
        # Retornar resultado
        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'message': 'There aren\'t any registers!'})
