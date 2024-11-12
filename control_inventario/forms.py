from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from datetime import date
from wtforms import Form, BooleanField, StringField, PasswordField, validators



class ProductosForm(FlaskForm):
    # Validador personalizado para asegurar que la fecha no sea futura
    def validate_fecha(form, field):
        if field.data > date.today():
            raise ValidationError("La fecha no puede ser en el futuro.")
    
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[
        DataRequired(message="La fecha es obligatoria."),
        validate_fecha
    ])

    proveedores = SelectMultipleField('Proveedores', coerce=int, validators=[
        DataRequired(message="Debe seleccionar al menos un proveedor.")
    ])

    categorias = SelectMultipleField('Categorias', coerce=int, validators=[
        DataRequired(message="Debe seleccionar al menos una categoria.")
    ])

    

    submit = SubmitField('Guardar')





class RegistrationForm(Form):
    nombre = StringField('registarnombre', [validators.Length(min=4, max=25)])
    apellidos = StringField('registrarapellido', [validators.Length(min=4, max=25)])
    genero = StringField('registrargenero', [validators.Length(min=4, max=25)])
    usuario = StringField('registrarusuario', [validators.Length(min=6, max=35)])
    password = PasswordField('registrarcontraseña', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])