import os
import datetime
from flask import Flask, render_template, url_for
from data import db_session
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.utils import redirect
from data.refactore_image import refactor_image

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
        f = form.avatar.data
        if f:
            file_way = os.getcwd() + f'\\static\\img\\avatars\\avatar_{user.id}.png'
            f.save(os.getcwd() + f'\\static\\img\\avatars\\avatar_{user.id}.png')
            refactor_image(file_way)
            user = session.query(User).filter(User.email == form.email.data).first()
            user.avatar = f'/static/img/avatars/avatar_{user.id}.png'
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
@app.route('/forum', methods=['GET', 'POST', 'DELETE', 'PUT'])
def records():
    session = db_session.create_session()
    news = session.query(News)
    comments = session.query(Comment)
    return render_template("records.html", news=news, comments=comments)


@app.route('/create_news', methods=['GET', 'POST'])
def create_news():
    form = NewsForm()

    param = dict()
    param['title'] = 'Добавление новости'
    param['style_way'] = url_for('static', filename='css/style.css')
    param['form'] = form
    param['template_name_or_list'] = 'news.html'
    param['back_way'] = '/forum'

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
    return render_template(**param)


@app.route('/refactor/<type>/<item_id>', methods=['GET', 'POST'])
def refactor(type, item_id):
    form = eval(type + 'Form()')
    session = db_session.create_session()

    item = session.query(eval(type)).filter(eval(type).id == item_id).first()
    param = dict()

    if not item:
        param['template_name_or_list'] = 'error.html'
        param['content'] = 'Данная запись не найдена'
        return render_template(**param)

    if item.user != current_user:
        param['template_name_or_list'] = 'error.html'
        param['content'] = 'Отказано в доступе'
        return render_template(**param)

    if form.validate_on_submit():
        item.content = form.content.data
        item.created_date = datetime.datetime.now()
        if type == 'News':
            item.title = form.title.data

        session.commit()

        return redirect('/forum')

    param['title'] = 'Изменение ' + 'новости' if type == 'News' else 'комментария'
    param['style_way'] = url_for('static', filename='css/style.css')
    param['form'] = form
    param['template_name_or_list'] = type.lower() + '.html'
    param['back_way'] = '/forum'

    if type == 'News':
        form.title.data = item.title
    form.content.data = item.content

    return render_template(**param)


@app.route('/delete/<type>/<item_id>')
def delete(type, item_id):
    session = db_session.create_session()
    item = session.query(eval(type)).filter(eval(type).id == item_id).first()
    param = dict()

    if not item:
        param['template_name_or_list'] = 'error.html'
        param['content'] = 'Данная запись не найдена'
        return render_template(**param)

    if item.user_id != current_user.id and current_user.status != 'admin':
        param['template_name_or_list'] = 'error.html'
        param['content'] = 'Отказано в доступе'
        return render_template(**param)

    session.delete(item)
    if type == 'News':
        comments = session.query(Comment).filter(Comment.news_id == item_id)
        for item in comments:
            session.delete(item)
    session.commit()
    return redirect('/forum')


@app.route('/create_comment/<news_id>/<user_id>', methods=['GET', 'POST'])
def create(news_id, user_id):
    form = CommentForm()

    param = dict()
    param['title'] = 'Добавление комментария'
    param['style_way'] = url_for('static', filename='css/style.css')
    param['form'] = form
    param['template_name_or_list'] = 'comment.html'
    param['back_way'] = '/forum' if user_id == '0' else f'/profile/{user_id}'

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
    return render_template(**param)


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


@app.route('/profile/<user_id>')
def profile(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    news = session.query(News).filter(News.user_id == user_id)
    comment = session.query(Comment).all()

    param = dict()
    param['title'] = user.name
    param['user'] = user
    param['news'] = news
    param['comments'] = comment
    param['template_name_or_list'] = 'profile.html'

    return render_template(**param)


@app.route('/make/<type>/<user_id>')
def make(type, user_id):
    param = dict()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        param['template_name_or_list'] = 'error.html'
        param['content'] = 'Пользователь не найден'
        return render_template(**param)

    if type == 'user' and (user.status == 'develop' and current_user.status != 'develop' or
                           user.status == 'admin' and current_user.status not in ('develop', 'admin')):
        param['template_name_or_list'] = 'error.html'
        param['content'] = 'Отказано в доступе'
        return render_template(**param)
    elif type == 'admin' and (user.status == 'develop' and current_user.status != 'develop' or
                              user.status == 'user' and current_user.status not in ('develop', 'admin')):
        param['template_name_or_list'] = 'error.html'
        param['content'] = 'Отказано в доступе'
        return render_template(**param)
    elif type == 'develop' and user.status in ('user', 'admin') and current_user.status != 'develop':
        param['template_name_or_list'] = 'error.html'
        param['content'] = 'Отказано в доступе'
        return render_template(**param)

    user.status = type
    session.commit()
    return redirect(f'/profile/{user_id}')


if __name__ == '__main__':
    main()
