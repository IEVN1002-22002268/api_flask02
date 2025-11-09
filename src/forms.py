from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, IntegerField
from wtforms import validators

""" heredado de la clase form mi funcion UserForm """
class UserForm(Form):
    matricula=IntegerField("Matricula", [
        validators.DataRequired(message = 'El campo es requerido')
    ])
    nombre = StringField("Nombre",[
        validators.DataRequired(message = 'El campo es requerido')
    ])
    apellido = StringField("Apellido",[
        validators.DataRequired(message = 'El campo es requerido')
    ])
    correo = EmailField("Correo",[
        validators.Email(message = "Ingrese correo válido")
    ])
