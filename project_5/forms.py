from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


def password_check(form, field):
    pass



class OrderForm(FlaskForm):
    name = StringField('Имя', [validators.InputRequired(message='Введите имя'),
                               validators.Length(min=1, max=25, message='Имя слишком длинное.')])
    phone = StringField('Телефон', [validators.InputRequired(message='Введите номер.'), validators.Length(min=12, max=12)])
    address = StringField('Адрес', [validators.InputRequired(message='Введите адрес.')])
    mail = StringField('Почта', [validators.Email(), validators.InputRequired(message='Введите email')])


class RegistrationForm(FlaskForm):
    mail = StringField('Почта', [validators.Email(), validators.InputRequired(message='Введите email.')])
    password = PasswordField('Пароль', [validators.InputRequired(message='Введите пароль.'),
                                        validators.Length(min=5, max=20, message="Пароль должен быть не менее 5 символов")])



class ChangePasswordForm(FlaskForm):
    pass


class LoginForm(FlaskForm):
    mail = StringField('Почта', [validators.Email(), validators.InputRequired(message='Введите email.')])
    password = PasswordField('Пароль', [validators.InputRequired(message='Введите пароль.'),
                                        validators.Length(min=5, max=20,
                                                          message="Пароль должен быть не менее 5 символов")])

