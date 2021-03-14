import uuid
import os

from flask import Flask
from flask import render_template, request, redirect, make_response, url_for
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from database import db_session, init_db
from login import login_manager
from models import User, Product

app = Flask(__name__)

app.secret_key = "ssucuuh398nuwetubr33rcuhne"

login_manager.init_app(app)
init_db()


@app.route('/')
def home():
    return render_template('home.html', current_user=current_user)


@app.route('/products')
@login_required
def products():
    role = current_user.get_role()
    return render_template("index.html", role=role, products=Product.query.all(), all=db_session.query(Product).count())


@app.route('/desc_r/<int:des_id>')
def description(des_id):
    review = Product.query.get(des_id)
    return render_template('desc_review.html', review=review)


@app.route('/login', methods=['GET', 'POST'])
def login():
    response = None
    if request.method == 'GET':
        response = make_response(render_template('login.html'))
    else:
        response = make_response(redirect(url_for('products')))
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            user.login_id = str(uuid.uuid4())
            db_session.commit()
            login_user(user)
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        profile_type = request.form.get("profile_type")
        user = User(username=username, password=password, profile_type=profile_type)
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('product.html')
    else:
        name = request.form['product_name']
        description = request.form['description']
        company = request.form['company']
        email = request.form['email']
        phone_number = request.form['phone_number']
        product = Product(name=name, description=description, company=company, email=email, phone_number=phone_number)
        db_session.add(product)
        db_session.commit()
        return redirect(url_for('products'))


if __name__ == '__main__':
    app.run()
