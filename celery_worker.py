from celery import Celery
from datetime import datetime
from model import Account, Currency, Transfer
import database

app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


def exchange(value, second_value):
    database.init_db()
    response_db = Currency.query.filter_by(currency_name=value, datatime='11-08-2022-23-51').first()
    second_response_db = Currency.query.filter_by(currency_name=second_value, datatime='11-08-2022-23-53').first()
    if response_db is None and second_response_db is None:
        return 'No currency to trade'
    return float(response_db.cost_concerning_USD / second_response_db.cost_concerning_USD)


@app.task
def task1(user_id, value, second_value, request_data):

    date_now = datetime.now().strftime('%d-%m-%Y')
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
            database.db_session.add(user_value_balance)
            database.db_session.add(exchange_currency)
            database.db_session.add(exchange_second_currency)
            database.db_session.add(user_second_value_balance)
            database.db_session.commit()
        except Exception:
            return 'Somethings go wrong'
        save_transfer = Transfer(
            user_name=user_id,
            type_of_transaction='exchange',
            amount_of_currency_spent=need_to_transfer,
            from_what_currency=value,
            in_what_currency=second_value,
            data_and_time=date_now,
            the_ammount_of_currency=trade_currency,
            donor_account=user_id.currency_id,
            beneficiary_account=user_id.currency_id,
        )
        try:
            database.db_session.add(save_transfer)
            database.db_session.commit()
        except Exception:
            return 'Fail data'
    else:
        return 'Err'
    return request_data['status']
