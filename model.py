from sqlalchemy import Column, Integer, String, Text, Float
from database import Base


class Account(Base):
    __tablename__ = 'Account'

    id = Column(String(10), primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    currency_name = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    user_deposit = Column(Integer)
    currency_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'currency_name': self.currency_name,
            'balance': self.balance,
            'user_deposit': self.user_deposit,
            'currency_id': self.currency_id
        }


class Currency(Base):
    __tablename__ = 'Currency'

    id = Column(Integer, primary_key=True, nullable=False)
    currency_name = Column(String, nullable=False)
    cost_concerning_USD = Column(Integer, nullable=False)
    available_quantity = Column(Integer, nullable=False)
    datatime = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'id': self.id,
            'currency_name': self.currency_name,
            'cost_concerning_USD': self.cost_concerning_USD,
            'available_quantity': self.available_quantity,
            'datatime': self.datatime

        }


class Deposit(Base):
    __tablename__ = 'Deposit'

    deposit_ID = Column(Integer, nullable=False, primary_key=True)
    opening_date = Column(String, nullable=False)
    closing_date = Column(String, nullable=False)
    value_name = Column(String)
    balance = Column(Float, nullable=False)
    interest_rate = Column(Integer, nullable=False)
    info = Column(String, nullable=False)
    id_user = Column(Integer, nullable=False)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'deposit_ID': self.deposit_ID,
            'opening_date': self.opening_date,
            'closing_date': self.closing_date,
            'value_name': self.value_name,
            'balance': self.balance,
            'interest_rate': self.interest_rate,
            'info': self.info,
            'id_user': self.id_user
        }


class History(Base):
    __tablename__ = 'History'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    history = Column(String)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'history': self.history
        }


class Rating(Base):
    __tablename__ = 'Rating'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    cur_name = Column(String, nullable=False)
    rating = Column(Integer)
    comment = Column(String)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'id': self.id,
            'cur_name': self.cur_name,
            'rating': self.rating,
            'comment': self.comment
        }


class Transfer(Base):
    __tablename__ = 'Transfer'

    user_name = Column(String, nullable=False)
    type_of_transaction = Column(String, nullable=False)
    amount_of_currency_spent = Column(Float, nullable=False)
    from_what_currency = Column(String, nullable=False)
    in_what_currency = Column(String, nullable=False)
    data_and_time = Column(String, nullable=False)
    the_ammount_of_currency = Column(Float, nullable=False)
    comission = Column(Integer)
    donor_account = Column(Integer, nullable=False)
    beneficiary_account = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_id = Column(Text)
    status = Column(Text)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'user_name': self.user_name,
            'type_of_transaction': self.type_of_transaction,
            'amount_of_currency_spent': self.amount_of_currency_spent,
            'from_what_currency': self.from_what_currency,
            'in_what_currency': self.in_what_currency,
            'data_and_time': self.data_and_time,
            'the_ammount_of_currency': self.the_ammount_of_currency,
            'comission': self.comission,
            'donor_account': self.donor_account,
            'beneficiary_account': self.beneficiary_account,
            'id': self.id
        }


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'id':  self.id,
            'login': self.login,
            'password': self.password
        }
