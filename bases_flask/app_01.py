
from flask import Flask, render_template, request
import math
import pizzeria.bases_flask.forms as forms
from flask import make_response, jsonify, json

app = Flask(__name__)
""" desde donde arrancará mi proyecto es lo que indica el ('/') """
@app.route('/index')
def index():
    titulo = "Pagina de inicio"
    listado = ['Python', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template('index.html', titulo = titulo, listado = listado)

""" mandar llamar la pagina por primera vez: tengo un get, se muestra sin valores """
""" mandar llamar a la pagina por segunda vez: un post que ya dibuja los valores """
@app.route('/calculos', methods=['GET','POST'])
def calculos():
    if request.method == 'POST':
        numero1 = request.form['numero1']
        numero2 = request.form['numero2']
        opcion = request.form['opcion']
        if opcion == 'suma':
            res = int(numero1) + int(numero2)
            signoop = '+'
        if opcion == 'resta':
            res = int(numero1) - int(numero2)
            signoop = '-'
        if opcion == 'multiplicacion':
            res = int(numero1) * int(numero2)
            signoop = '*'
        if opcion == 'division':
            res = int(numero1) / int(numero2)
            signoop = '/'
        return render_template('calculos.html', res=res, numero1=numero1, numero2=numero2, signoop=signoop)
    return render_template('calculos.html')

@app.route('/distancia', methods=['GET','POST'])
def distancia():
    if request.method == 'POST':
        numerox1 = request.form['numerox1']
        numerox2 = request.form['numerox2']
        numeroy1 = request.form['numeroy1']
        numeroy2 = request.form['numeroy2']
        operacionX = int(numerox2) - int((numerox1))
        operacionY = int(numeroy2) - int((numeroy1))
        xCuadrada = math.pow(operacionX, 2)
        yCuadrada = math.pow(operacionY, 2)
        sumaDeXyY = xCuadrada + yCuadrada
        res = int(math.sqrt(sumaDeXyY))
        return render_template('distancia.html', numerox1=numerox1, numerox2=numerox2,
                            numeroy1=numeroy1, numeroy2=numeroy2, res=res)
    return render_template('distancia.html')

@app.route('/Alumnos', methods=['GET','POST'])
def alumnos():
    mat = 0
    nom=""
    ape=""
    email=""
    tem=[]
    estudiantes=[]
    datos=()
    alumno_clase=forms.UserForm(request.form)
    
    if request.method == 'POST' and alumno_clase.validate():
        if request.form.get("btnElimina")=='eliminar':
            response = make_response(render_template('Alumnos.html',))
            response.delete_cookie('usuario')
        mat=alumno_clase.matricula.data
        nom=alumno_clase.nombre.data
        ape=alumno_clase.apellido.data
        email=alumno_clase.correo.data

        datos={'matricula':mat,'nombre':nom.rstrip(),
               'apellido':ape.rstrip(),'email':email.rstrip()}  
        
        data_str = request.cookies.get("usuario")
        if not data_str:
             return "No hay cookie guardada", 404
        estudiantes = json.loads(data_str)
        estudiantes.append(datos)  
    response=make_response(render_template('Alumnos.html',
        form=alumno_clase, mat=mat, nom=nom, apell=ape, email=email))

    if request.method!='GET':
        response.set_cookie('usuario', json.dumps(estudiantes))
    return response

@app.route("/get_cookie")
def get_cookie():
    data_str = request.cookies.get("usuario")
    if not data_str:
        return "No hay cookie guardada", 404
    estudiantes = json.loads(data_str)
    return jsonify(estudiantes)

""" variable tipo string llamada user """
@app.route('/user/<string:user>')
def user(user):
    return f"Hello, {user}!"

@app.route('/numero/<int:num>')
def func(num):
    return f"El numero es: {num}"

@app.route('/suma/<int:num1>/<int:num2>')
def suma(num1, num2):
    return f"La suma es: {num1 + num2}"

""" La ruta user recibe dos parametros diferentes, entonces 
NO se confundira con la del user de la de arriba. Lo ÚNICO que
debe ser diferente es que el metodo debe ser diferente """
@app.route('/user/<int:id>/<string:username>')
def username(id, username):
    return "ID: {} - Nombre: {}".format(id,username)

@app.route('/suma/<float:n1>/<float:n2>')
def func1(n1, n2):
    return "La suma es: {}".format(n1+n2)

@app.route('/default/')
@app.route('/default/<string:dft>')
def func2(dft="sss"):
    return "El valor de dft es: "+dft

""" ----------------------------- Hoy 18 de octubre ----------------------------- """
@app.route("/prueba")
def func4():
    return ''' 
    <html>
        <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
            <title>Pagina Prueba</title>
        </head>
        <body>
            <h1>Hola, esta es una página de prueba</h1>
            <p>Esta página es para probar el retorno de HTML en Flask</p>
        </body>
    </html> 
'''


""" crear sistema de arranque del proyecto """
if __name__ == '__main__':
    app.run(debug=True)