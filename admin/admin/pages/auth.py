import datetime

from flask import request, flash, redirect, url_for, Response, current_app
from flask_admin import BaseView, expose
from flask_admin.menu import MenuLink
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.routing import BuildError
from wtforms import StringField, validators, PasswordField, BooleanField, \
    ValidationError, SubmitField

from string import digits, ascii_lowercase

from database.engine import get_db
from database.models import Employee

alphabet = digits + ascii_lowercase + '_'

db = get_db()


class LoginLink(MenuLink):
    def is_visible(self):
        return not current_user.is_authenticated

    def is_accessible(self):
        return not current_user.is_authenticated

    def get_url(self):
        return url_for('login.index')


class LogoutLink(MenuLink):
    def is_visible(self):
        return current_user.is_authenticated

    def is_accessible(self):
        return current_user.is_authenticated

    def get_url(self):
        return url_for('login.logout')


class LoginForm(FlaskForm):
    login = StringField(
        label='Login',
        validators=[validators.DataRequired()],
        description='Username',
    )
    password = PasswordField(
        label='Password',
        validators=[validators.DataRequired()],
        description='Password from account',
    )
    remember = BooleanField(label='Remember session')

    submit = SubmitField(label='Login')

    class Meta:
        csrf = True

    def validate_login(self, field: StringField):
        if any(filter(lambda i: i not in alphabet, field.data)):
            raise ValidationError('Login is incorrect! ')


def redirect_dest(fallback) -> Response:
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
        return redirect(dest_url)
    except (BuildError, TypeError):
        return redirect(fallback)


class LoginView(BaseView):
    def is_visible(self):
        return False

    @expose('/', methods=('GET', 'POST'))
    def index(self):

        if current_user.is_authenticated:
            print('logined')
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate_on_submit():
            employee = db.session.query(Employee).filter_by(
                login=form.login.data).first()
            print(employee)
            if not employee or not employee.check_password(
                    password=form.password.data):
                flash('Wrong login data!')
                return self.render('admin_panel/login.html', form=form)
            login_user(
                employee,
                remember=form.remember.data,
                duration=datetime.timedelta(days=30)
            )
            return redirect_dest(fallback=url_for('admin.index'))
        return self.render('admin_panel/login.html', form=form)

    @expose('/logout')
    def logout(self):
        current_app.logger.info('Logout')
        logout_user()
        flash('Logout')
        return redirect(url_for('login.index'))
