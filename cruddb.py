from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm #, DataRequired, Length
from wtforms import StringField, SubmitField, PasswordField, EmailField
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# User model (replace with your actual schema)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário:') #, validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email:') #, validators=[DataRequired(), EmailField()])
    password = PasswordField('Senha:') #, validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Cadastrar')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))  # Change to desired route after successful registration
    return render_template('cadastrar.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)