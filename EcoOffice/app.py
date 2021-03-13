import uuid
import os

from flask import Flask
from flask import render_template, request, redirect, make_response, url_for
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import logging
from flask_bootstrap import Bootstrap


from database import db_session, init_db
from login import login_manager
from models import User
from models import Product

app = Flask(__name__)

app.secret_key = "ssucuuh398nuwetubr33rcuhne"

login_manager.init_app(app)
init_db()


@app.route('/')
def home():
    #role = current_user.get_role()
    # return render_template("index.html", role=role)
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    response = None
    if request.method == 'GET':
        response = make_response(render_template('login.html'))
    else:
        response = make_response(redirect(url_for('home')))
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


@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        return render_template('product.html')
    else:
        username = request.form['username']
        description = request.form['password']
        company = request.form['company']
        product = Product(username=username, description=description, company=company)
        db_session.add(product)
        db_session.commit()
        response = make_response(redirect(url_for('home')))
        return response

@app.route('/home')
def list_all():
    return render_template('index.html', products=Product.all())





if __name__ == '__main__':
    app.run()
