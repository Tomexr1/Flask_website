from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


app = Flask(__name__, static_folder='static', static_url_path='/static')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "mysecret"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    liked = db.Column(db.String(1000), nullable = True)

db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def hello_world():
    return redirect(url_for('home'))

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            if request.form.get('username') and request.form.get('password'):
                user = Users.query.filter_by(username=request.form.get('username')).first()
                if user:
                    flash('Nazwa użytkownika zajęta')
                    return redirect(url_for('sign_up'))
                new_user = Users(username=request.form.get('username'), password=request.form.get('password'))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
        return render_template('sign_up.html')
    else:
        return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            user = Users.query.filter_by(username=request.form.get('username')).first()
            if user:
                if user.password == request.form.get('password'):
                    login_user(user)
                    if 'url' in session:
                        return redirect(session['url'])
                    return redirect(url_for('home'))
                else:
                    flash('Złe hasło')
                    return redirect(url_for('login'))
            else:
                flash('Nie ma takiego użytkownika')
                return redirect(url_for('login'))
        return render_template('login.html')
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home'))

@app.route('/home')
def home():
    session['url'] = url_for('home')
    return render_template('home.html')

@app.route('/przyklady_wyk', methods=['GET', 'POST'])
def przyklady_wyk():
    if current_user.is_authenticated:
        pos = ""
        if request.method == 'POST':
            if request.form.get('zapisz'):
                pos = request.form.get('zapisz')
                user = Users.query.filter_by(username=current_user.username).first()
                if user.liked:
                    liked_list = list(user.liked.split(','))
                    if request.form.get('zapisz') not in liked_list:
                        liked_list.append(request.form.get('zapisz'))
                        user.liked = ','.join(liked_list)
                        flash('Dodano do ulubionych')
                else:
                    user.liked = request.form.get('zapisz')
                    flash('Dodano do ulubionych')
                db.session.commit()
                flash('Dodano do ulubionych')
            if request.form.get('usun'):
                pos = request.form.get('usun')
                user = Users.query.filter_by(username=current_user.username).first()
                liked_list = list(user.liked.split(','))
                if request.form.get('usun') in liked_list:
                    liked_list.remove(request.form.get('usun'))
                    user.liked = ','.join(liked_list)
                    db.session.commit()
                flash('Usunięto z ulubionych')
        session['url'] = url_for('przyklady_wyk')
        if pos:
            return render_template('przyklady_wyk.html', pos=pos)
        else:
            return render_template('przyklady_wyk.html')
    else:
        session['url'] = url_for('przyklady_wyk')
        return render_template('przyklady_wyk.html')

@app.route('/przyklady_log', methods=['GET', 'POST'])
def przyklady_log():
    if current_user.is_authenticated:
        pos = ""
        if request.method == 'POST':
            if request.form.get('zapisz'):
                pos = request.form.get('zapisz')
                user = Users.query.filter_by(username=current_user.username).first()
                if user.liked:
                    liked_list = list(user.liked.split(','))
                    if request.form.get('zapisz') not in liked_list:
                        liked_list.append(request.form.get('zapisz'))
                        user.liked = ','.join(liked_list)
                        flash('Dodano do ulubionych')
                else:
                    user.liked = request.form.get('zapisz')
                    flash('Dodano do ulubionych')
                db.session.commit()
                flash('Dodano do ulubionych')
            if request.form.get('usun'):
                pos = request.form.get('usun')
                user = Users.query.filter_by(username=current_user.username).first()
                liked_list = list(user.liked.split(','))
                if request.form.get('usun') in liked_list:
                    liked_list.remove(request.form.get('usun'))
                    user.liked = ','.join(liked_list)
                    db.session.commit()
                flash('Usunięto z ulubionych')
        session['url'] = url_for('przyklady_log')
        if pos:
            return render_template('przyklady_log.html', pos=pos)
        else:
            return render_template('przyklady_log.html')
    else:
        session['url'] = url_for('przyklady_log')
        return render_template('przyklady_log.html')

@app.route('/o_projekcie')
def projekt():
    session['url'] = url_for('projekt')
    return render_template('o_projekcie.html')

@app.route('/o_autorach')
def autorzy():
    session['url'] = url_for('autorzy')
    return render_template('o_autorach.html')



if __name__ == '__main__':
    app.run(debug=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 5
    app.config["TEMPLATES_AUTO_RELOAD"] = True