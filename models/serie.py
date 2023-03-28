from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder


class Serie():
    def __init__(self, id=None, serie=None, ndoc=None) -> None:
        self.id = id
        self.serie = serie
        self.ndoc = ndoc

    def list_serie(self, tc_id):
      # Abrir conexion a la base de datos
        con = db().open
        # Crear un cursor
        cursor = con.cursor()
        # Preparar la consulta
        sql = "select id, serie, ndoc from serie where tipo_comprobante_id=%s"
        # Ejecutar la consulta sql
        cursor.execute(sql, [tc_id])
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
