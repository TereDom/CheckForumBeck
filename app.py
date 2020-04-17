import datetime
from flask import Flask, render_template
from data import db_session
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.utils import redirect
from data.LoginForm import LoginForm
from data.RegisterForm import RegisterForm
from data.__all_models import User, WikiDB
from data.NewsForm import NewsForm


from data.__all_forms import *
from data.__all_models import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('db/DataBase.sqlite')


def main():
    app.run(port=8000, host='127.0.0.1')


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
            return redirect('/forum')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/forum', methods=['GET', 'POST', 'DELETE', 'PUT'])
def records():
    session = db_session.create_session()
    news = session.query(News)
    comments = session.query(Comment)
    return render_template("records.html", news=news, comments=comments)


@app.route('/new_news',  methods=['GET', 'POST'])
def new_news():
    form = NewsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = News(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        session.merge(current_user)
        session.add(news)
        session.commit()
        return redirect('/forum')
    return render_template('news.html', title='Добавление новости', form=form)


@app.route('/refactor_news/<news_id>', methods=['GET', 'POST'])
def refactor_news(news_id):
    form = NewsForm()
    session = db_session.create_session()

    news = session.query(News).filter(News.id == news_id).first()

    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        news.created_date = datetime.datetime.now()

        session.commit()

        return redirect('/forum')

    form.title.data = news.title
    form.content.data = news.content

    return render_template('news.html', title='Изменение новости', form=form)


@app.route('/delete_news/<news_id>')
def delete_news(news_id):
    session = db_session.create_session()
    news = session.query(News).filter(News.id == news_id).first()
    session.delete(news)
    comments = session.query(Comment).filter(Comment.news_id == news_id)
    for item in comments:
        session.delete(item)
    session.commit()
    return redirect('/forum')


@app.route('/create_comment/<news_id>', methods=['GET', 'POST'])
def create_comment(news_id):
    form = CommentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            news_id=news_id
        )
        session.merge(current_user)
        session.add(comment)
        session.commit()
        return redirect('/forum')
    return render_template('comment.html', title='Добавление комментария', form=form)


@app.route('/refactor_comment/<comment_id>', methods=['GET', 'POST'])
def refactor_comment(comment_id):
    form = CommentForm()
    session = db_session.create_session()

    comment = session.query(Comment).filter(Comment.id == comment_id).first()

    if form.validate_on_submit():
        comment.content = form.content.data

        session.commit()
        return redirect('/forum')

    form.content.data = comment.content

    return render_template('comment.html', title='Изменение комментария', form=form)


@app.route('/wiki', methods=['GET', 'POST', 'DELETE', 'PUT'])
def wiki():
    return render_template('general_wiki.html')


@app.route('/wiki/<status>')
def print_wiki(status):
    session = db_session.create_session()
    wiki_base = session.query(WikiDB)
    return render_template('wiki.html', title='Энциклопедия CheckBeck',
                           wiki_base=wiki_base, status=status)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/forum")


if __name__ == '__main__':
    main()
