from flask import Flask, render_template, request
import forms
from flask import make_response, jsonify, json

app = Flask(__name__)

@app.route('/Pizzeria', methods=['GET', 'POST'])
def pizzeria():
    pedido_pizza=[]
    cliente_info={}
    ventas_totales_lista=[]
    total_ventas_dia=0.0

    pedido_cookie = request.cookies.get('pedido_temporal')
    if pedido_cookie:
        pedido_pizza = json.loads(pedido_cookie)
    
    ventas_cookie = request.cookies.get('cookie_ventas')
    if ventas_cookie:
        ventas_totales_lista = json.loads(ventas_cookie)

    cliente_cookie=request.cookies.get('cliente_temporal')
    if cliente_cookie:
        cliente_info=json.loads(cliente_cookie)

    #mi clase forms de la pizza
    pizza_form=forms.PizzeriaForm(request.form)

    if request.method=='POST':
        accion=request.form.get('accion')
        if accion=='Agregar':
            if pizza_form.validate():
                if pizza_form.tamanio.data and pizza_form.numPizzas.data:
                    tamanio_valor = float(pizza_form.tamanio.data)
                    num_pizzas = int(pizza_form.numPizzas.data)
                    costo_ingredientes = 0
                    nombres_ingredientes = []

                    if pizza_form.jamon.data: 
                        costo_ingredientes=costo_ingredientes + 10
                        nombres_ingredientes.append('jamón')
                    if pizza_form.pina.data: 
                        costo_ingredientes=costo_ingredientes + 10
                        nombres_ingredientes.append('piña')
                    if pizza_form.champinones.data: 
                        costo_ingredientes=costo_ingredientes + 10
                        nombres_ingredientes.append('champiñones')

                    subtotal=(tamanio_valor+costo_ingredientes)*num_pizzas

                    tamanio_texto=""
                    for valor, texto in pizza_form.tamanio.choices:
                        if valor==pizza_form.tamanio.data:
                            tamanio_texto=texto
                            break
                    ingredientes_texto = ""
                    for ingredientes in nombres_ingredientes:
                        ingredientes_texto = ingredientes_texto + ingredientes + ". "
                    
                    pizza={'tamanio_texto':tamanio_texto, 'ingredientes':ingredientes_texto,
                        'num_pizzas':num_pizzas, 'subtotal':subtotal}
                    pedido_pizza.append(pizza)
                    
                    cliente_info={'nombre':pizza_form.nombre.data, 'direccion':pizza_form.direccion.data,
                        'telefono':pizza_form.telefono.data}
                    response = make_response(render_template('Pizzeria.html',
                        form=pizza_form, pedido_pizza=pedido_pizza, ventas_acumuladas=ventas_totales_lista, total_ventas_dia=total_ventas_dia)) 
                    
                    #estas son las cookies temporales
                    response.set_cookie('pedido_temporal', json.dumps(pedido_pizza))
                    response.set_cookie('cliente_temporal', json.dumps(cliente_info))
                    return response
                
        elif accion=='Quitar':
            if pedido_pizza:
                pedido_pizza.pop()
            response=make_response(render_template('Pizzeria.html', form=pizza_form, 
                pedido_pizza=pedido_pizza, ventas_acumuladas=ventas_totales_lista, 
                total_ventas_dia=total_ventas_dia))
            response.set_cookie('pedido_temporal', json.dumps(pedido_pizza))
            return response

        elif accion=='Terminar':
            total_pedido_final=0
            #total pero por persona
            for p in pedido_pizza:
                total_pedido_final=total_pedido_final+p.get('subtotal', 0)
            #agregar el total por persona con sus datos personales
            if total_pedido_final>0 and cliente_info:
                venta={'nombre':cliente_info.get('nombre'), 'direccion':cliente_info.get('direccion'),
                    'telefono':cliente_info.get('telefono'), 'total':total_pedido_final}
                
                ventas_totales_lista.append(venta)
                pedido_pizza=[] 

            #suma total de los totales de los clientes
            total_ventas_dia=0
            for v in ventas_totales_lista:
                total_ventas_dia=total_ventas_dia+v.get('total', 0)

            response=make_response(render_template('Pizzeria.html', form=pizza_form, 
                pedido_pizza=pedido_pizza, ventas_acumuladas=ventas_totales_lista, total_ventas_dia=total_ventas_dia))
            #cookie ventas la que si se guarda en la aplicacion
            response.set_cookie('cookie_ventas', json.dumps(ventas_totales_lista))
            response.delete_cookie('pedido_temporal')
            response.delete_cookie('cliente_temporal')
            return response

    total_ventas_dia = 0
    for v in ventas_totales_lista:
        total_ventas_dia = total_ventas_dia+v.get('total', 0)

    response = make_response(render_template('Pizzeria.html', form=pizza_form, pedido_pizza=pedido_pizza,
        ventas_acumuladas=ventas_totales_lista, total_ventas_dia=total_ventas_dia))
    return response

@app.route("/get_pedido_cookie")
def get_pedido_cookie():
    data_str= request.cookies.get("pedido_temporal")
    if not data_str:
        return "No hay cookie de pedido guardada", 404
    pedido = json.loads(data_str)
    return jsonify(pedido)
@app.route("/get_ventas_cookie")
def get_ventas_cookie():
    data_str = request.cookies.get("cookie_ventas")
    if not data_str:
        return "No hay cookie de ventas guardada", 404
    ventas = json.loads(data_str)
    return jsonify(ventas)
@app.route("/get_cliente_cookie")
def get_cliente_cookie():
    data_str = request.cookies.get("cliente_temporal")
    if not data_str:
        return "No hay cookie de cliente guardada", 404
    cliente = json.loads(data_str)
    return jsonify(cliente)

if __name__ == '__main__':
    app.run(debug=True)