from flask import Flask

from admin.admin_conf import register_admin
from database.engine import get_db
from database.models import Employee
from login_manager import get_login_manager


def register_shell_context(flask_app: Flask):
    def shell_context():
        db = get_db()
        return {
            'db': db,
            'Employee': Employee,
        }
    flask_app.shell_context_processor(shell_context)


def create_app(config: dict) -> Flask:
    db = get_db()
    flask_app = Flask(
        __name__,
        static_url_path='',
        static_folder='frontend/static',
        template_folder='frontend/templates',
    )
    flask_app.config.update(**config)
    register_admin(flask_app=flask_app, database=db)
    register_shell_context(flask_app)
    login_manager = get_login_manager()
    login_manager.init_app(flask_app)
    db.init_app(app=flask_app)
    return flask_app
