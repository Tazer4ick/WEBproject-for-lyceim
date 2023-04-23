from flask import Flask, redirect, render_template, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session
from helpers.CONSTS import PATH_TO_DATABASE, HOST, PORT, BASE_API_URL

from models.resources import news_resources, users_resources

from models.users import User
from models.news import News

from models.forms.news_forms import NewsForm
from models.forms.user_forms import LoginForm, RegisterForm

from requests import get, post, delete, put

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init(PATH_TO_DATABASE)

    # API resources
    api.add_resource(news_resources.NewsListResource, '/api/news')
    api.add_resource(news_resources.NewsResource, '/api/news/<int:news_id>')
    api.add_resource(users_resources.UsersListResource, '/api/users')
    api.add_resource(users_resources.UsersResource, '/api/users/<int:user_id>')

    app.run(host=HOST, port=PORT)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = post(f"{BASE_API_URL}/news",
                    json={
                        'title': form.title.data,
                        'content': form.content.data,
                        'is_private': form.is_private.data,
                        'user_id': current_user.get_id()
                    })
        if news.status_code == 200:
            return redirect('/')
        else:
            return render_template('news.html', title='Добавление новости', form=form,
                                   message="Что-то пошло не так")
    return render_template('news.html', title='Добавление новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    url = f"{BASE_API_URL}/news/{id}"
    url += f"?is_authenticated={current_user.is_authenticated}&user_id={current_user.get_id()}"
    news = delete(url)
    if news.status_code == 200:
        return redirect('/')
    elif news.status_code == 403:
        abort(403, message=news.json())
    else:
        abort(404, message=news.json())
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        url = f"{BASE_API_URL}/news/{id}"
        url += f"?is_authenticated={current_user.is_authenticated}&user_id={current_user.get_id()}"
        news = get(url)
        if news.status_code == 200:
            news = news.json()['news']
            form.title.data = news['title']
            form.content.data = news['content']
            form.is_private.data = news['is_private']
        else:
            return render_template('news.html', title='Редактирование новости',
                                   message="Новость не найдена")
    if form.validate_on_submit():
        news = put(f"{BASE_API_URL}/news/{id}",
                   json={
                       'title': form.title.data,
                       'content': form.content.data,
                       'is_private': form.is_private.data,
                       'user_id': current_user.get_id()
                   })
        if news.status_code == 200:
            return redirect('/')
        elif news.status_code == 403:
            return render_template('news.html', title='Редактирование новости',
                                   message="У вас нет прав на редактирование", form=form)
        else:
            return render_template('news.html', title='Редактирование новости',
                                   message="Новость не найдена", form=form)
    return render_template('news.html', title='Редактирование новости', form=form)


@app.route("/")
def index():
    news = get(f"{BASE_API_URL}/news?is_authenticated={current_user.is_authenticated}&user_id={current_user.get_id()}")
    if news.status_code == 200:
        news = news.json()['news']
        for i in range(len(news)):
            news[i]['user']['id'] = str(news[i]['user']['id'])
        return render_template("index.html", news=news)
    else:
        return render_template("index.html", message="Что-то пошло не так")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user = post(f"{BASE_API_URL}/users",
                           json={
                               "name": form.name.data,
                               "about": form.about.data,
                               "email": form.email.data,
                               "hashed_password": form.password.data,
                               "password_again": form.password_again.data
                           })
        if create_user.status_code == 409:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        elif create_user.status_code == 400:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        elif create_user.status_code == 200:
            return redirect('/login')
        else:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Что-то пошло не так")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()

