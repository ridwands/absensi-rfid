from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager


login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = 'iloveu'
#app.permanent_session_lifetime = datetime.timedelta(days=365)
CORS(app)
login_manager.init_app(app)