from flask import Flask, flash, redirect,\
render_template, request,url_for
from flask_cors import CORS, cross_origin

import utils 
from valorant import ValorantAPI

app = Flask(__name__)
app.secret_key = 'a{:":}s^&*6ank1^!!221&*2'
cors = CORS(app)

@app.route('/', methods=['GET', 'POST'])
@cross_origin(allow_headers=['*'])
def login():
    return render_template('login.html')

@app.route('/submit', methods=['GET', 'POST'])
@cross_origin(allow_headers=['*'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')
    region = request.form.get('region')
    mandatory_params=[username,password,region]

    if utils.validate_input(mandatory_params):
        client_ip = utils.get_client_ip(request)
        try:
            valorant_login = ValorantAPI(username, password, region, client_ip)
            skins = valorant_login.player_store
            return render_template('skins.html', skins=skins)
        except Exception as error:
            flash(str(error)+'; Please try again')
            return redirect(url_for('login'))
    else:
        flash('Username/Password/Region cannot be empty')
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug='true')
