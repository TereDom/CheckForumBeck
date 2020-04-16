from flask import Flask, render_template
from data import db_session
from flask_login import login_user, LoginManager, current_user
from werkzeug.utils import redirect
from data.LoginForm import LoginForm
from data.RegisterForm import RegisterForm
from data.__all_models import User, WikiDB
from data.NewsForm import NewsForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init('db/DataBase.sqlite')
    app.run(port=8080, host='127.0.0.1')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data,
                    email=form.email.data,
                    vk_id=form.vk_id.data)

        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
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


@app.route('/wiki', methods=['GET', 'POST', 'DELETE', 'PUT'])
def wiki():
    return render_template('general_wiki.html')


@app.route('/wiki/<status>')
def print(status):
    session = db_session.create_session()
    wiki_base = session.query(WikiDB)
    return render_template('wiki.html', title='Энциклопедия CheckBeck',
                           wiki_base=wiki_base, status=status)


@app.route('/')
def index():
    return "CheckForumBeck"


if __name__ == '__main__':
    main()