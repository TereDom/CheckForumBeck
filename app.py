from flask import Flask, render_template
from data import db_session
from flask_login import login_user
from werkzeug.utils import redirect
from data.LoginForm import LoginForm
from data.RegisterForm import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run(port=8080, host='127.0.0.1')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # session = db_session.create_session()
        # if session.query(User).filter(User.email == form.email.data).first():
        #     return render_template('register.html', title='Регистрация',
        #                            form=form,
        #                            message="Такой пользователь уже есть")
        # user = User(
        #     name=form.name.data,
        #     email=form.email.data,
        #     about=form.about.data
        # )
        # user.set_password(form.password.data)
        # session.add(user)
        # session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     session = db_session.create_session()
    #     user = session.query(User).filter(User.email == form.email.data).first()
    #     if user and user.check_password(form.password.data):
    #         login_user(user, remember=form.remember_me.data)
    #         return redirect("/")
    #     return render_template('login.html',
    #                            message="Неправильный логин или пароль",
    #                            form=form)
    return render_template('login.html', title='Авторизация', form=form)

from flask import Flask, render_template
from data import db_session
from flask_login import login_user, login_required
from werkzeug.utils import redirect
from data.LoginForm import LoginForm
from data.RegisterForm import RegisterForm
from data.NewsForm import NewsForm



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run(port=8080, host='127.0.0.1')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # session = db_session.create_session()
        # if session.query(User).filter(User.email == form.email.data).first():
        #     return render_template('register.html', title='Регистрация',
        #                            form=form,
        #                            message="Такой пользователь уже есть")
        # user = User(
        #     name=form.name.data,
        #     email=form.email.data,
        #     about=form.about.data
        # )
        # user.set_password(form.password.data)
        # session.add(user)
        # session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     session = db_session.create_session()
    #     user = session.query(User).filter(User.email == form.email.data).first()
    #     if user and user.check_password(form.password.data):
    #         login_user(user, remember=form.remember_me.data)
    #         return redirect("/")
    #     return render_template('login.html',
    #                            message="Неправильный логин или пароль",
    #                            form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/forum', methods=['GET', 'POST', 'DELETE', 'PUT'])
def records():
    # session = db_session.create_session()
    # news = session.query(News).filter(News.is_private != True)
    return render_template("records.html")


@app.route('/news',  methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        # session = db_session.create_session()
        # news = News()
        # news.title = form.title.data
        # news.content = form.content.data
        # news.is_private = form.is_private.data
        # current_user.news.append(news)
        # session.merge(current_user)
        # session.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()