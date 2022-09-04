import datetime


from flask import Flask, request
from flask_migrate import Migrate

import model
from sqlalchemy import create_engine

from model import db
from model import Currency, Account, Rating, Transfer, User, History, Deposit


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@127.0.0.1:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.get("/Currency/<value_name>/rating")
def feedback(value_name):
    response_db = db.session.query(
            db.func.avg(model.Rating.rating)
    ).filter(
            model.Rating.cur_name == value_name
    ).first()

    return f'{value_name}' f' avg: {response_db}'


@app.post("/Currency/<value_name>/rating")
def currency_rating(value_name):
    request_data = request.json
    comment = request_data['comment']
    rating = request_data['rating']
    response_db = Rating(
        value_name=value_name,
        comment=comment,
        rating=rating
    )
    try:
        db.session.add(response_db)
        db.session.commit()
    except Exception:
        return 'Err'
    return response_db['status']


@app.get("/Currency/<value_name>")
def show_currency(value_name):
    response_db = Currency.query.filter_by(currency_name=value_name).all()
    return [itm.to_dict() for itm in response_db]


@app.get("/Currency/trade/<value>/<second_value>")
def exchange(value, second_value):
    response_db = Currency.query.filter_by(currency_name=value, datatime='11-08-2022-23-51').first()
    second_response_db = Currency.query.filter_by(currency_name=second_value, datatime='11-08-2022-23-53').first()
    if response_db is None and second_response_db is None:
        return 'No currency to trade'
    return {
        'exchange': response_db.cost_concerning_USD / second_response_db.cost_concerning_USD
    }


@app.post("/Currency/trade/user_id/<value>/<second_value>")
def trade(user_id, value, second_value):
    request_data = request.json['ammount']
    date_now = datetime.datetime.now().strftime('%d-%m-%Y')

    trade_currency = exchange(value, second_value)

    user_value_balance = Account.query.filter_by(user_id=user_id, currency_name=value).first()
    user_second_value_balance = Account.query.filter_by(user_id=user_id, currency_name=second_value).first()
    if user_value_balance is None or user_second_value_balance is None:
        return f'{user_id} don`t have {value} '

    need_to_transfer = round(request_data / float(trade_currency), 2)

    exchange_currency = Currency.query.filter_by(currency_name=value, datatime=date_now).first()
    exchange_second_currency = Currency.query.filter_by(currency_name=value, datatime=date_now).first()

    if float(user_value_balance.balance) > exchange_currency and (
            float(exchange_second_currency.available_quantity) > need_to_transfer
    ):

        user_value_balance.balance = float(user_value_balance.balance) - exchange_currency
        exchange_currency.available_quantity = float(exchange_currency.available_quantity) + exchange_currency
        exchange_second_currency.available_quantity = float(
            exchange_second_currency.available_quantity) - trade_currency
        user_second_value_balance.balance = float(user_second_value_balance.balance) + trade_currency

        try:
            db.session.add(user_value_balance)
            db.session.add(exchange_currency)
            db.session.add(exchange_second_currency)
            db.session.add(user_second_value_balance)
            db.session.commit()
        except Exception:
            return 'Somethings go wrong'

        save_transfer = Transfer(
            user_id=user_id,
            type_of_transaction='exchange',
            ammount_of_currency_spent=exchange_currency,
            from_what_currency=value,
            in_what_currency=second_value,
            data_and_time=date_now,
            the_ammount_of_currency=trade_currency,
            donor_account=user_id.currency_id,
            beneficiary_account=user_id.currency_id,

        )
        try:
            db.session.add(save_transfer)
            db.session.commit()
        except Exception:
            return 'Fail data'
    else:
        return 'Err'
    return request_data['status']


@app.get("/Currency")
def home_page():
    result = Currency.query.all()
    return [itm.to_dict() for itm in result]


@app.get("/User/<user_id>")
def user_page(user_id):
    response_data = db.session.query(model.User, model.Account).join(
        model.User, model.User.id == model.Account.user_id).filter_by(login=user_id).all()
    return {
        'Test': f'{response_data}'
    }


@app.post("/User/transfer")
def user_transfer():
    pass


@app.get("/User/<user_name>/history")
def user_history(user_name):
    response_db = Transfer.query.filter_by(user_name=user_name).all()
    return {
        'history': f'{response_db}'
    }


@app.post("/User/deposit/<user_name>")
def user_deposit(user_name):
    response_db = request.json
    deposit = Deposit(
        id_user=user_name,
        deposit_id=response_db['deposit_id'],
        opening_date=response_db['data']['opening_data'],
        closing_data=response_db['data']['closing_data'],
        value_name=response_db['value_name'],
        balance=response_db['balance'],
        interest_rate=response_db['data']['interest_rate'],
        info=response_db['data']['info']
    )
    try:
        db.session.add(deposit)
        db.session.commit()
    except Exception:
        return 'Something go wrong'
    else:
        return response_db['status']


@app.get("/User/deposit/<user_name>")
def choose_deposit(user_name):
    response_db = Deposit.query.filter_by(id_user=user_name).all()
    if len(response_db) == 0:
        return 'You don`t have deposit'
    return {
        'Data': f'{response_db}'
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
