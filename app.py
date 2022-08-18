from flask import Flask
from flask import request

import sqlite3 as db

from datetime import datetime

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


@app.get("/Currency/<value_name>/rating")
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


@app.get("/Currency/trade/<value>/<second_value>")
def exchange(value, second_value):
    response_db = get_data(f'''select round(
    (select cost_concerning_USD from Currency where currency_name= "{value}" order by datatime DESC limit 1)/
    (select cost_concerning_USD from Currency where currency_name= "{second_value}" order by datatime DESC limit 1), 2)
    as exchange_value''')
    return response_db


@app.post("/Currency/trade/<user_id>/<value>/<second_value>")
def trade(user_id, value, second_value):
    amount = request.get_json()['amount']
    user_balance = get_data(f'select balance from Account where user_id = "{user_id}" and currency_name= "{value}"')
    user_balance_second = get_data(
        f'select balance from Account where user_id = "{user_id}" and currency_name= "{second_value}"')

    avaliable_currency_value = get_data(
        f'select * from Currency where currency_name = "{second_value}" order by datatime desc limit 1')
    value_cost_per_one = avaliable_currency_value[0]['cost_concerning_USD']

    avaliable_currency_second_value = get_data(
        f'select * from Currency where currency_name = "{second_value}" order by datatime desc limit 1')
    second_value_cost_per_one = avaliable_currency_second_value[0]['cost_concerning_USD']

    needed_second_value = amount * 1.0 * value_cost_per_one / second_value_cost_per_one

    exists_second_value_currency = avaliable_currency_second_value[0]['avaliable_quantity']
    if (user_balance[0]['balance'] >= amount) and (exists_second_value_currency > needed_second_value):
        get_data(
            f'update Currency set available_quantity = {exists_second_value_currency - needed_second_value} where datatime ={avaliable_currency_second_value[0]["datetime"]} and currency_name = {second_value}')
        get_data(
            f'update Currency set available_quantity = {avaliable_currency_value[0]["avaliable_quantity"] + amount} where datatime ={avaliable_currency_second_value[0]["datetime"]} and currency_name = {value}')
        spent = get_data(
            f'update Account set balance = {user_balance[0]["balance"] - amount} where user_id ={user_id} and currency_name = {value}')
        recive = get_data(
            f'update Account set  balance = {user_balance_second[0]["balance"] + needed_second_value} where user_id ={user_id} and currency_name = {second_value}')

        get_data(f'''insert into Transfer 
        (type_of_transaction, amount_of_currency_spent, from_what_currency, in_what_currency, data_and_time, the_ammount_of_currency, donor_account, beneficiary_account) values 
        ({"exchange"}, {spent}, {value}, {second_value}, {"17.08.2022, 23:52"}, {recive}, {user_id}, {"FRANSUA SHOVINP`YE"})''')


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
