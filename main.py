from flask import Flask, request, render_template, session, redirect
from pymongo import MongoClient
from colorama import Fore
import random


app = Flask(__name__, static_folder = "static/css")
client = MongoClient('mongodb://localhost:27017/')
db = client['users']
app.secret_key = "secreat_key"


class Host():
    def random_port() -> int:
        return random.randint(1000,9999)

    host = '127.0.0.1'
    port = random_port()


class Colors():
    err = f'{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}ERROR{Fore.LIGHTBLACK_EX}] {Fore.LIGHTWHITE_EX}'
    success = f'{Fore.LIGHTBLACK_EX}[{Fore.LIGHTGREEN_EX}SUCCESS{Fore.LIGHTBLACK_EX}] {Fore.LIGHTWHITE_EX}'
    warning = f'{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}WARNING{Fore.LIGHTBLACK_EX}] {Fore.LIGHTWHITE_EX}'


class Main(object):
    @app.route('/home')
    @app.route('/index')
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        if('username' in session):
            uname = session['username']
            user = db.users.find_one({'username': uname})
            return render_template('dashboard.html',
                                   uploads = user['uploads'],
                                   stars = user['stars'],
                                   days = 10)
        else:
            return redirect('/')
        
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/login_sys', methods = ['POST'])
    def login_sys():
        username = request.form['username']
        password = request.form['password']

        user = db.users.find_one({'username': username, 'password': password})

        if(user):
            session['username'] = username
            return render_template('dashboard.html',
                                   uploads = user['uploads'],
                                   stars = user['stars'],
                                   days = 10)
        else:
            print(f'{Colors.err} Wrong username or password!')
            return render_template('login.html', error = 'Wrong username or password!')
        
    @app.route('/register_sys', methods = ['POST'])
    def register_sys():
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user_exist = db.users.find_one({'username': username})

        if(user_exist):
            print(f'{Colors.err} Username is already exist!')
            return render_template('register.html', error = 'Username is already exist!')
        else:
            session['username'] = username

            db.users.insert_one({
                'username': username, 
                'password': password,
                'email': email,
                'role': 'user',
                'uploads': 0,
                'stars': 0
            })

            return render_template('dashboard.html', stars = 0, uploads = 0, days = 0)
        
    @app.route('/logout')
    def logout():
        session.pop('username', None)
        print(f'{Colors.success} The user has logged out.')
        return redirect('/index')
    
    @app.route('/upload', methods = ['POST'])
    def upload():
        username = session['username']
        text_content = request.form['textContent']
        title = request.form['title']
        user = db.users.find_one({'username': username})

        if(user):
            current_value = user.get('uploads', 0)
            new_value = current_value + 1
            
            db.users.update_one({'username': username}, {'$set': {'uploads': new_value}})

            print(f'{Colors.success} The post has been added!')
            user = db.users.find_one({'username': username})

            f = open(f'{title}.html', 'a')
            f.write(f'{text_content}')
            f.close()

            return render_template('dashboard.html',
                                success = 'The post has been added!',
                                stars = user['stars'], 
                                uploads = user['uploads'], 
                                days = 10)
        else:
            print(f'{Colors.err} The user does not exist.')
            return render_template('dashboard.html', error = 'The user does not exist!')
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
        

if(__name__ == '__main__'):
    app.run(host = Host.host, port = Host.port, debug = True)