from flask import Flask
from flask import request
app = Flask(__name__)


@app.route("/currency/<value_name>/review", methods=['GET', 'POST', 'PUT', 'DELETE'])
def feedback():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    else:
        pass


@app.get("/currency/<value_name>")
def show_currency():
    pass


@app.route("/currency/trade/<value>/<second_value>", methods=['GET', 'POST'])
def exchange():
    if request.method == 'GET':
        pass
    else:
        pass


@app.get("/currency")
def home_page():
    pass


@app.get("/user")
def user_page():
    pass


@app.post("/user/transfer")
def user_transfer():
    pass


@app.get("/user/history")
def user_histroy():
    pass


@app.route("/user/deposit", methods=['GET', 'POST'])
def user_deposit():
    if request.method == 'GET':
        pass
    else:
        pass


@app.get("/user/deposit/<deposit_id>")
def deposit():
    pass


@app.get("/deposit/<value_name>")
def choose_deposit():
    pass
