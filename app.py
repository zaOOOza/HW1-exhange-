import os
import sqlalchemy
from flask import Flask, request, session

from datetime import datetime
from random import randint

import model
import database
from model import Currency, Rating, Transfer, Deposit
from celery_worker import task1

app = Flask(__name__)

session_secret = os.environ.get('SESSION_SECRET')
if not session_secret:
    if not os.path.exists('session.secret'):
        secret_file = open('session.secret', 'w')
        secret_file.write(str(randint(10000000, 999999999)))
        secret_file.close()
    secret_file = open('session.secret')
    session_secret = secret_file.read()
    secret_file.close()

app.secret_key = session_secret


@app.get("/Currency/<value_name>/rating")
def feedback(value_name):
    database.init_db()
    response_db = database.db_session.query(
        sqlalchemy.func.avg(model.Rating.rating)
    ).filter(
        model.Rating.cur_name == value_name
    ).first()

    return f'{value_name}' f' avg: {response_db}'


@app.post("/Currency/<value_name>/rating")
def currency_rating(value_name):
    request_data = request.json
    comment = request_data['comment']
    rating = request_data['rating']
    database.init_db()
    response_db = Rating(cur_name=value_name, comment=comment, rating=rating)
    try:
        database.db_session.add(response_db)
        database.db_session.commit()
    except Exception:
        return 'Err'
    return response_db['status']


@app.get("/Currency/<value_name>")
def show_currency(value_name):
    database.init_db()
    response_db = Currency.query.filter_by(currency_name=value_name).all()
    return [itm.to_dict() for itm in response_db]


@app.get("/Currency/trade/<value>/<second_value>")
def exchange(value, second_value):
    database.init_db()
    response_db = Currency.query.filter_by(currency_name=value, datatime=datetime.now()).first()
    second_response_db = Currency.query.filter_by(currency_name=second_value, datatime=datetime.now()).first()
    if response_db is None and second_response_db is None:
        return 'No currency to trade'
    return {
        'exchange': response_db.cost_concerning_USD / second_response_db.cost_concerning_USD
    }


@app.post("/Currency/trade/user_id/<value>/<second_value>")
def trade(user_id, value, second_value):
    request_data = request.form.get('ammount')
    task_obj = task1.apply_async(args=[user_id, value, second_value, request_data])
    return {'trade_id': str(task_obj)}


@app.get("/Currency")
def home_page():
    database.init_db()
    result = Currency.query.all()
    return [itm.to_dict() for itm in result]


@app.route("/User", methods=['GET', 'POST'])
def user_page():
    database.init_db()
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id is None:
            return '''
            <html>
             <form method="post">
 

  <div class="container">
    <label for="uname"><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="uname" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>

    <button type="submit">Login</button>
  </div>
</form> 
            </html>
            '''
        else:
            response_data = database.db_session.query(model.User, model.Account).join(
                model.User, model.User.id == model.Account.user_id).filter_by(login=user_id).all()
            return {
                'Test': f'{response_data}'
            }
    if request.method == 'POST':
        user_login = request.form.get('uname')
        user_password = request.form.get('psw')
        user_info_creds = model.User.query.filter_by(login=user_login, password=user_password).all()
        if user_info_creds:
            session['user_id'] = user_login
            return 'Deal with it'
        else:
            'bad gataway'



@app.post("/User/transfer")
def user_transfer():
    pass


@app.get("/User/<user_name>/history")
def user_history(user_name):
    database.init_db()
    response_db = Transfer.query.filter_by(user_name=user_name).all()
    return {
        'history': f'{response_db}'
    }


@app.post("/User/deposit/<user_name>")
def user_deposit(user_name):
    response_db = request.json
    database.init_db()
    deposit = Deposit(
        id_user=user_name,
        deposit_ID=response_db['deposit_id'],
        opening_date=response_db['data']['opening_data'],
        closing_date=response_db['data']['closing_data'],
        value_name=response_db['value_name'],
        balance=response_db['balance'],
        interest_rate=response_db['data']['interest_rate'],
        info=response_db['data']['info']
    )
    try:
        database.db_session.add(deposit)
        database.db_session.commit()
    except Exception:
        return 'Something go wrong'
    else:
        return response_db['status']


@app.get("/User/deposit/<user_name>")
def choose_deposit(user_name):
    database.init_db()
    response_db = Deposit.query.filter_by(id_user=user_name).all()
    if len(response_db) == 0:
        return 'You don`t have deposit'
    return {
        'Data': f'{response_db}'
    }


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
