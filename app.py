from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__, static_folder='static', static_url_path='/static')


@app.route('/')
def hello_world():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/przyklady_wyk')
def przyklady_wyk():
    return render_template('przyklady_wyk.html')

@app.route('/przyklady_log')
def przyklady_log():
    return render_template('przyklady_log.html')

@app.route('/o_projekcie')
def projekt():
    return render_template('o_projekcie.html')

@app.route('/o_autorach')
def autorzy():
    return render_template('o_autorach.html')



if __name__ == '__main__':
    app.run(debug=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 5
    app.config["TEMPLATES_AUTO_RELOAD"] = True