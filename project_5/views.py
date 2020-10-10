from flask import abort, session, redirect, render_template

import datetime

from project_5 import app, db
from project_5.models import User, Meal, Category, Order
from project_5.forms import OrderForm, RegistrationForm, LoginForm

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Order, db.session))


@app.route('/')
def main():
    categories = db.session.query(Category).all()
    meals = db.session.query(Meal).order_by(db.func.random())
    return render_template('main.html', categories=categories, meals=meals, Meal=Meal)


@app.route('/cart/<deleted>/', methods=["GET", "POST"])
def cart(deleted):
    if deleted != 'f' and deleted != 't':
        abort(404)
    form = OrderForm()
    meals = db.session.query(Meal)
    if form.validate_on_submit():
        if not session.get('total_price', False):
            form.mail.errors.append('Заказ не может быть пустым')
            return render_template('cart.html', form=form, meals=meals, Meal=Meal)
        mail = form.mail.data
        user = db.session.query(User).filter(User.mail == mail).first()
        phone = form.phone.data
        address = form.address.data
        data = datetime.datetime.today().date()
        meals_titles = []
        for meal_id in session.get('cart'):
            meals_titles.append(db.session.query(Meal).get(meal_id).title)
        ordered = Order(phone=phone, address=address, mail=mail, data=data, price=int(session['total_price']),
                        user=user, ord_meals=','.join(meals_titles), status='Выполняется')
        db.session.add(ordered)
        db.session.commit()
        return redirect('/ordered/')
    return render_template('cart.html', form=form, meals=meals, Meal=Meal, deleted=deleted)


@app.route('/addtocart/<int:item_id>')
def addtocart(item_id):
    cart = session.get('cart', [])
    try:
        check = db.session.query(Meal).get(item_id).price
    except AttributeError:
        abort(404)
    else:
        cart.append(item_id)
        session['cart'] = cart
        total_price = 0
        for id in session['cart']:
            total_price += db.session.query(Meal).get(id).price
        session['total_price'] = total_price
        return redirect('/cart/f')


@app.route('/delete/<int:id>')
def delete(id):
    cart = session.get('cart', [])
    if id not in cart:
        return redirect('/cart/f')
    cart.remove(id)
    deleted = 't'
    session['cart'] = cart
    total_price = 0
    for id in session['cart']:
        total_price += db.session.query(Meal).get(id).price
    session['total_price'] = total_price
    return redirect('/cart/t')


@app.route('/account/')
def account():
    if session.get('user', False):
        orders = db.session.query(Order).filter(Order.user_id == session['user']['id']).all()
        meals = db.session.query(Meal)
        return render_template('account.html', orders=orders, meals=meals, Meal=Meal)
    return redirect('/login/')


@app.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.mail == form.mail.data).first()
        if user and user.password_valid(form.password.data):
            session['user'] = {'id': user.id, 'is_auth': True}
            return redirect('/account/')
        else:
            form.password.errors.append('Неверное имя пользователя или пароль')
    return render_template('login.html', form=form)


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if db.session.query(User).filter(User.mail == form.mail.data).first() is not None:
            mess = 'Указанный email уже используется, пожалуйста, укажите другой почтовый адрес.'
            form.mail.errors.append(mess)
            return render_template('register.html', form=form)
        user = User(mail=form.mail.data, status='user')
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect('/register_done/')
    return render_template('register.html', form=form)


@app.route('/register_done/')
def register_done():
    return render_template('register_complited.html')


@app.route('/logout/')
def logout():
    if session.get('user', False):
        remove_user = session.pop('user')
    return redirect('/')


@app.route('/ordered/')
def ordered():
    return render_template('ordered.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404', error=error), 404

