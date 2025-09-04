import os
from flask import Flask
from flask_login import LoginManager
from routes import setup_routes
from models import User

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your-secret-key'  # Replace with a secure key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import Base
    engine = create_engine('sqlite:///qms.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session.query(User).get(int(user_id))

setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
