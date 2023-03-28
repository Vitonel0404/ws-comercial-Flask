from flask import Flask


#Importar a los módulos que contienen a los servicios web
from ws.sesion import ws_sesion
from ws.producto import ws_producto
from ws.cliente import ws_cliente
from ws.venta import ws_venta 
from ws.tipo_comprobante import ws_tipo_comprobante
from ws.serie import ws_serie
from ws.configuracion import ws_configuracion
#Crear la variable de aplicación con Flask
app = Flask(__name__)


#Registrar los módulos que contienen a los servicios web
app.register_blueprint(ws_sesion)
app.register_blueprint(ws_producto)
app.register_blueprint(ws_cliente)
app.register_blueprint(ws_venta)
app.register_blueprint(ws_tipo_comprobante)
app.register_blueprint(ws_serie)
app.register_blueprint(ws_configuracion)


@app.route('/')
def home():
    return 'Servicios web en ejecución'

#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=3000, debug=True, host='0.0.0.0')
