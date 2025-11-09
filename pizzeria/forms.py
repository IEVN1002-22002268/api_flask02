from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, IntegerField, RadioField
from wtforms import validators

class PizzeriaForm(Form):
    nombre = StringField("Nombre",[
        validators.DataRequired(message = 'El campo es requerido')
    ])
    direccion = StringField("Direccion",[
        validators.DataRequired(message = 'El campo es requerido')
    ])
    telefono = StringField("Telefono",[
        validators.DataRequired(message = 'El campo es requerido')
    ])
    tamanio = RadioField('Tamaño Pizza', choices=[('40', 'Chica $40'),('80', 'Mediana $80'),('120', 'Grande $120')],
        validators=[validators.Optional()])
    
    jamon = BooleanField('Jamon 10$')
    pina = BooleanField('Piña 10$')
    champinones = BooleanField('Champiñones 10$')

    numPizzas=IntegerField("Num. de Pizzas", [
        validators.Optional()
    ])
