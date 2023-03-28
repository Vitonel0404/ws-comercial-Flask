from MySQLdb import cursors
from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Venta:
    def __init__(self, cliente_id=None, tipo_comprobante_id=None, nser=None, ndoc=None,fdoc=None,sub_total=None,igv=None,total=None, porcentaje_igv=None,usuario_id_registro=None, almacen_id=None, detalle_venta=None):
        self.cliente_id=cliente_id
        self.tipo_comprobante_id=tipo_comprobante_id
        self.nser=nser
        self.ndoc=ndoc
        self.fdoc=fdoc
        self.sub_total=sub_total
        self.igv=igv
        self.total=total
        self.porcentaje_igv=porcentaje_igv
        self.usuario_id_registro=usuario_id_registro
        self.almacen_id=almacen_id
        self.detalle_venta=detalle_venta
    
    def insertar(self):
        con= db().open
        #indicar que los cambios realizados en la bd se confimarán de forma manual
        con.autocommit=False

        cursor= con.cursor()
        #obtener el número de documento a emitir segun la serie
        sql="SELECT ndoc+1 as nuevodoc FROM serie WHERE serie=%s"
        cursor.execute(sql,[self.nser])
        nuevo_documento = cursor.fetchone()
        self.ndoc=nuevo_documento['nuevodoc']

        #prapara la sentencia sql para insert de la tabla venta
        sql="insert into venta(cliente_id,tipo_comprobante_id,nser,ndoc,fdoc,sub_total,igv,total,porcentaje_igv,usuario_id_registro,almacen_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            #ejecutar la sentencia sql que inserta en la tabla venta
            cursor.execute(sql,[ self.cliente_id, self.tipo_comprobante_id,self.nser,self.ndoc, self.fdoc,self.sub_total,self.igv,self.total,self.porcentaje_igv,self.usuario_id_registro, self.almacen_id])

             #Obtener el id de la venta que se ha registrado para grabarlo en la tabla venta_detalle
            venta_id = con.insert_id()

            # Recoger los datos que vienen de la venta en formato json
            jsonArrayDetalleVenta = json.loads(self.detalle_venta)

            #Recorrer datos en el array 

            for detalle in jsonArrayDetalleVenta:
                #Preparar la consulta SQL para insertar en venta detalle
                sql="INSERT INTO venta_detalle(venta_id,producto_id,cantidad,precio,importe) values(%s,%s,%s,%s,%s)"

                producto_id= detalle["producto_id"]
                cantidad = detalle["cantidad"]
                precio = detalle["precio"]
                importe = float(cantidad) * float(precio)

                #Ejecutar la sentencia sql
                cursor.execute(sql, [venta_id,producto_id,cantidad,precio,importe])

                #Preparar la sentencia sql para actualizar el stock del producto ventido en el amacen que corresponda
                sql_stock = "UPDATE stock_almacen SET stock = stock-%s WHERE producto_id = %s and almacen_id = %s"

                cursor.execute(sql_stock,[cantidad,producto_id,self.almacen_id])

            #actualizar el numero de docuemtno (ndoc) en la tabla serie
            sql= "update serie set ndoc=%s where serie=%s"
            cursor.execute(sql,[self.ndoc, self.nser])

            #confirmar los cambios registrados en la bd
            con.commit()

            #retornar respuesta satisfactoria
            return json.dumps({'status':True,'data':'La venta se a registrado correctamente','ndoc':self.ndoc})
        
        except con.Error as error:
            #Revocar todas instrucciones sql ejecutadas en la bd 
            con.rollback()
            #retornar un mensaje de error error al usuario
            return json.dumps({'status':False,'data':format(error)},cls=CustomJsonEncoder)
        finally:
            cursor.close()
            con.close()
