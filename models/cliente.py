from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Cliente():
    def __init__(self, id=None, nombre=None, direccion=None,email=None,ciudad_id=None):
        self.id=id
        self.nombre=nombre
        self.direccion=direccion
        self.email=email
        self.ciudad_id=ciudad_id
    
    def listaCliente(self):
        con = db().open
        cursor = con.cursor()
        sql="select id,nombre from cliente order by nombre"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursor.close()
        con.close()
        
        if datos:
            return json.dumps({'status':True, 'data':datos},cls=CustomJsonEncoder)
        else:
            return json.dumps({'status':False,'data':'No hay registros'})