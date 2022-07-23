from flask_login import LoginManager

from database.engine import get_db
from database.models import Employee


def get_login_manager():
    db = get_db()
    login = LoginManager()
    login.user_loader(lambda user_id: db.session.query(Employee).get(user_id))
    return login