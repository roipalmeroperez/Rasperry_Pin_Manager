from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
# Configuración para MariaDB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://roi:pinmanagerpass@localhost/develop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registro de usuarios
@app.route('/register', methods=['GET'])
def registerWeb():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    new_user = User(username=request.form['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return "Usuario registrado con éxito"

# Inicio de sesión
from flask_login import login_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
        #user = request.form['username']
        #if user == "roi" and request.form['password'] == "pass":
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        return "Credenciales incorrectas"
    else:
        return render_template('login.html')

from flask_login import login_required
@app.route('/')
@login_required
def dashboard():
    return "Contenido principal protegido por contraseña"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas automáticamente en MariaDB
    app.run(debug=True)
