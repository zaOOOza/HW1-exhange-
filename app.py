from flask import Flask
from flask import request

import sqlite3 as db

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_data(query: str):
    con = db.connect('exchange.db')
    con.row_factory = dict_factory
    cursor = con.execute(query)
    result = cursor.fetchall()
    con.commit()
    con.close()
    return result


@app.route("/Currency/<value_name>/rating")
def feedback(value_name):
    response_db = get_data(f'select round(avg(rating), 2), cur_name from Rating where cur_name="{value_name}"')
    return response_db


@app.post("/Currency/<value_name>/rating")
def currency_rating(value_name):
    request_data = request.get_json()
    comment = request_data['comment']
    rating = request_data['rating']
    get_data(f' insert into Rating (cur_name, rating, comment) values ("{value_name}", "{rating}", "{comment}")')
    return 'ok'


@app.get("/Currency/<value_name>")
def show_currency(value_name):
    response_db = get_data(f'select * from Currency where currency_name = "{value_name}"')
    return response_db


@app.route("/Currency/trade/<value>/<second_value>", methods=['GET', 'POST'])
def exchange(value, second_value):
    if request.method == 'GET':
        response_db = get_data(f'''select round(
        (select cost_concerning_USD from Currency where datatime="11.08.2021" and currency_name="{value}")/
        (select cost_concerning_USD from Currency where datatime="11.08.2021" and currency_name="{second_value}"), 2)
        as exchange_value''')
        return response_db
    else:
        pass


@app.get("/Currency")
def home_page():
    response_db = get_data(f' select * from Currency')
    return response_db


@app.get("/User/<user_id>")
def user_page(user_id):
    response_db = get_data(f'select User.login, Account.currency_name, Account.balance, Account.user_deposit, '
                           f'Account.currency_id from User join Account where User.id=Account.user_id = {user_id}')
    return response_db


@app.post("/User/transfer")
def user_transfer():
    pass


@app.get("/User/history/<user_name>")
def user_history(user_name):
    response_db = get_data(f'select history from History where user_name ="{user_name}"')
    return response_db


@app.route("/User/deposit/<deposit_id>", methods=['GET', 'POST'])
def user_deposit(deposit_id):
    if request.method == 'GET':
        response_db = get_data(f'select user_deposit from Account where user_deposit="{deposit_id}" ')
        return response_db
    else:
        pass


@app.get("/Deposit/<deposit_value>")
def choose_deposit(deposit_value):
    response_db = get_data(f'select * from Deposit where value_name="{deposit_value}"')
    return response_db
