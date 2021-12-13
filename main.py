from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from UserLogin import UserLogin
import bd
import pyshorteners
import requests

bd.connect()

app = Flask(__name__)

menu = [{"name": "Регистрация ", "url": "register"}, 
        {"name": "Авторизация ", "url": "auth"},
        {"name": "Сократить", "url": "profile"},
        {"name": "Мои ссылки", "url": "links"}]

app.secret_key = 'xxxxyyyyyzzzzz'

login_manager = LoginManager(app)
login_manager.login_view = 'auth'
login_manager.login_message = "Авторизуйтесь, чтобы сократить ссылку, или увидеть сокращённые ссылки!!!"

@login_manager.user_loader
def check_user(user_id):
    print(user_id)
    return UserLogin().fromDB(user_id, bd)

@app.route("/short", methods=["POST", "GET"])
@login_required
def short():
    try:
        name = request.form.get('name')
        url = request.form.get("url")
        shortURL = pyshorteners.Shortener().tinyurl.short(url)
        access = request.form.get('access')
        links = bd.getLinks(current_user.get_id())
        msg = ""
        r=requests.head(shortURL)
        
        if url != links[0][2] and current_user.get_id() != links[0][5]:
            bd.addLink(name, url, shortURL, access, current_user.get_id())
            msg = f"Сокращённая ссылка: {shortURL}, Право доступа: {access}, Исходная ссылка: {url}\n"
            flash(msg)
            if access == "Приватная":  
                r.is_redirect = False
        elif url == links[0][2] and current_user.get_id() == links[0][5]:
            msg = "Вы уже сокращали эту ссылку!!!"
            flash(msg)
        
        return render_template('profile.html', title='Авторизация', menu = menu)
    except Exception as e:
        return f"Ошибка: {e}"


@app.route("/links", methods=["POST", "GET"])
@login_required
def myLinks():
    try:
        msg = []
        links = bd.getLinks(current_user.get_id())
        for link in links:
            print(link)
            msg.append(f"Сокращённая ссылка: {link[3]}    Право доступа: {link[4]}    Исходная ссылка: {link[2]}   Короткое имя: {link[1]}")
            print(msg)
        flash(msg)
       
        
        return render_template('links.html', title='Авторизация', menu = menu)
    except Exception as e:
        return f"Ошибка: {e}"



@app.route('/')
def index():
   return render_template("index.html", menu=menu, title="Главная") 


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        user = bd.checkUser(request.form['login'])
        print("!!!!!!!!")
        print(user)
        if user == 0:
            flash('Такого пользователя не существует!')
        elif user and check_password_hash(user[2], request.form['password']):
            print("!!!!!!!!")
            userLogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userLogin, remember=rm)
            return redirect(url_for('profile'))
        else:
            flash('Неверные данные!')
    return render_template('auth.html', title='Авторизация', menu = menu)


@app.route('/register', methods=['POST', 'GET'])
def register():
    print(url_for('register'))
    if request.method == 'POST':
        if len(request.form['password']) >= 4 and len(request.form['login']) >= 4:
            hash = generate_password_hash(request.form['password'])
            reg = bd.checkUser(request.form['login'])
            
            if reg == 0:
                bd.reg(request.form['login'], hash)
                flash("Вы зарегистрировались!")
                redirect(url_for('auth'))
            else:
                flash("Вы уже регистрировались")
        else:
            flash('Неверное заполнение полей! (Пароль и Логин должны быть больше 3 символов)')
    return render_template('register.html', title='Регистрация', menu = menu)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('auth'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Авторизация', menu = menu)

if __name__=="__main__":
    app.run()