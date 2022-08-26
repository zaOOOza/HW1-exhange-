from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'Account'

    id = db.Column(db.String(10), db.ForeignKey("user_id"), unique=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    currency_name = db.Column(db.String, nullable=False)
    balance = db.Column(db.REAL, nullable=False)
    user_deposit = db.Column(db.Integer)
    currency_id = db.Column(db.Integer, nullable=False)

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


class Currency(db.Model):
    __tablename__ = 'Currency'

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    currency_name = db.Column(db.String, nullable=False)
    cost_concerning_USD = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    datatime = db.Column(db.String, nullable=False)

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


class Deposit(db.Model):
    __tablename__ = 'Deposit'

    deposit_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    opening_date = db.Column(db.String, nullable=False)
    closing_date = db.Column(db.String, nullable=False)
    value_name = db.Column(db.String)
    balance = db.Column(db.REAL, nullable=False)
    interest_rate = db.Column(db.Integer, nullable=False)
    info = db.Column(db.String, nullable=False)
    id_user = db.Column(db.Integer, nullable=False)

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


class History(db.Model):
    __tablename__ = 'History'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable=False)
    history = db.Column(db.String)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'history': self.history
        }


class Rating(db.Model):
    __tablename__ = 'Rating'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    cur_name = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'id': self.id,
            'cur_name': self.cur_name,
            'rating': self.rating,
            'comment': self.comment
        }


class Transfer(db.Model):
    __tablename__ = 'Transfer'

    user_name = db.Column(db.String, nullable=False)
    type_of_transaction = db.Column(db.String, nullable=False)
    amount_of_currency_spent = db.Column(db.REAL, nullable=False)
    from_what_currency = db.Column(db.String, nullable=False)
    in_what_currency = db.Column(db.String, nullable=False)
    data_and_time = db.Column(db.String, nullable=False)
    the_ammount_of_currency = db.Column(db.REAL, nullable=False)
    comission = db.Column(db.Integer)
    donor_account = db.Column(db.Integer, nullable=False)
    beneficiary_account = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

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


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'{self.to_dict()}'

    def to_dict(self):
        return {
            'id':  self.id,
            'login': self.login,
            'password': self.password
        }