from flask import Flask, render_template, request
import math
import src.forms as forms

app = Flask(__name__)
""" desde donde arrancará mi proyecto es lo que indica el ('/') """
@app.route('/index')
def index():
    titulo = "Pagina de inicio"
    listado = ['Python', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template('index.html', titulo = titulo, listado = listado)

@app.route('/Alumnos', methods=['GET','POST'])
def alumnos():
    mat = 0
    nom=""
    ape=""
    email=""
    """ crear instancia de la clase """
    alumno_clase=forms.UserForm(request.form)
    if request.method == 'POST' and alumno_clase.validate():
        mat=alumno_clase.matricula.data
        nom=alumno_clase.nombre.data
        ape=alumno_clase.apellido.data
        email=alumno_clase.correo.data
        """ render template no se repite porque las VARIABLES están declaradas ANTES del method POST """
    return render_template('Alumnos.html', form=alumno_clase, mat=mat, nom=nom, ape=ape, email=email)
