from MySQLdb import cursors
from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Producto():
    def __init__(self, id =None, nombre=None, precio=None, categoria_id=None):
        self.id=id
        self.nombre=nombre
        self.precio=precio
        self.categoria_id=categoria_id
    
    def listarProductosCatalogos(self, almacen_id):
        #abrir conexion a la base de datos
        con=db().open
        cursor=con.cursor()
        sql="SELECT p.id, p.nombre, p.precio, c.nombre as categoria, s.stock, a.nombre as almacen, concat('/static/imgs-producto/', p.id, '.jpg') as img FROM producto p INNER JOIN categoria c ON (p.categoria_id = c.id) INNER JOIN stock_almacen s ON (s.producto_id = p.id) INNER JOIN almacen a ON (a.id = s.almacen_id) WHERE s.almacen_id =%s ORDER BY p.nombre"
        #    SELECT p.id, p.nombre, p.precio, c.nombre AS categoria, s.stock FROM producto p INNER JOIN categoria c ON (p.categoria_id = c.id) INNER JOIN stock_almacen s ON (s.producto_id = p.id) WHERE s.almacen_id = 1
        #ejecutar consulta
        cursor.execute(sql,[almacen_id])
        #capturar los datos que devuelve la consulta sql
        datos =cursor.fetchall()
        cursor.close()
        con.close()
        if datos:
            return json.dumps({'status':True,'data':datos},cls=CustomJsonEncoder)
        else:
            return json.dumps({'status':False,'data':'No hay registros'})
    



