from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Warwick-IFP'
global n
n = 0


class AccountForm(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()])
    password = StringField('Set PIN - it should be 4 digits', validators=[DataRequired()])
    password_again = StringField('Repeat your PIN again', validators=[DataRequired()])
    submit = SubmitField('Create an account')


class MoneyDepositForm(FlaskForm):
    account_number = StringField('Your account number', validators=[DataRequired()])
    password = StringField('PIN', validators=[DataRequired()])
    money = StringField('How much money you want to deposit', validators=[DataRequired()])
    submit = SubmitField('Deposit money')


class MoneyWithdrawForm(FlaskForm):
    account_number = StringField('Your account number', validators=[DataRequired()])
    password = StringField('PIN', validators=[DataRequired()])
    money = StringField('How much money you want to deposit', validators=[DataRequired()])
    submit = SubmitField('Deposit money')


class BalanceForm(FlaskForm):
    account_number = StringField('Your account number', validators=[DataRequired()])
    password = StringField('PIN', validators=[DataRequired()])
    submit = SubmitField('Show my Balance')


@app.route('/', methods=['GET', 'POST'])
def starter():
    if request.method == 'POST':
        if request.form.get('action'):
            return redirect('/deposit')
        elif request.form.get('action') == 'withdraw':
            return redirect('/withdraw')
        elif request.form.get('action') == 'balance':
            return redirect('/balance')
    return render_template('main.html', title='Main page')


@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    con = sqlite3.connect("database/ATM_database.db")
    cur = con.cursor()
    form = MoneyDepositForm()
    if form.validate_on_submit():
        res = cur.execute(
            f"SELECT id, user_id, account_number, deposit, PIN FROM accounts WHERE account_number IS "
            f"'{form.account_number.data}'").fetchone()
        if not res:
            return render_template('deposit.html', title='Deposit', form=form, message="Account doesn't exist")
        if form.password.data != str(res[4]):
            return render_template('deposit.html', title='Deposit', form=form, message='Incorrect PIN')
        cur.execute(f"UPDATE accounts SET deposit='{int(res[3]) + int(form.money.data)}'")
        con.commit()
        return render_template('deposit.html', title='Deposit', form=form, suc='SUCCESS')
    return render_template('deposit.html', title='Deposit', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    con = sqlite3.connect("database/ATM_database.db")
    cur = con.cursor()
    form = AccountForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('signup.html', title='Account Creation', form=form, message="PINs are different")
        elif len(form.password.data) != 4:
            return render_template('signup.html', title='Account Creation', form=form, message="PIN must be 4 digits")
        elif not (form.password.data.isdigit()):
            return render_template('signup.html', title='Account Creation', form=form, message="PIN must be 4 digits")
        res = cur.execute(f"SELECT id FROM user_data WHERE user_name IS '{form.name.data}'").fetchone()
        if res:
            num = cur.execute(f"SELECT account_number FROM accounts WHERE user_id IN "
                              f"(SELECT id FROM user_data WHERE user_name IS '{form.name.data}')").fetchone()[0]
            return render_template('signup.html', title='Account Creation', form=form,
                                   message=f"You are already in the system, your account number - {num}")
        cur.execute(
            f"INSERT INTO user_data(user_name, creation_date) VALUES ('{form.name.data}', '{datetime.date.today()}')")
        global n
        with open('data/account_num.txt') as file:
            n = int(file.readline())
        n += 1
        with open('data/account_num.txt', 'w') as file:
            file.write(str(n))
        cur.execute(
            f"INSERT INTO accounts(user_id, account_number, pin) VALUES ((SELECT id FROM user_data WHERE user_name IS '{form.name.data}'), "
            f"'{n}', '{form.password.data}')")
        con.commit()
        return render_template('signup.html', title='Account Creation', form=form)
    return render_template('signup.html', title='Account Creation', form=form)


@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html', title='Deposit', account_num=n)


@app.route('/balance', methods=['GET', 'POST'])
def balance():
    con = sqlite3.connect("database/ATM_database.db")
    cur = con.cursor()
    form = BalanceForm()
    if form.validate_on_submit():
        res = cur.execute(
            f"SELECT id, user_id, account_number, deposit, PIN FROM accounts WHERE account_number IS "
            f"'{form.account_number.data}'").fetchone()
        if not res:
            return render_template('balance.html', title='Balance', form=form, message="Account doesn't exist")
        if form.password.data != str(res[4]):
            return render_template('balance.html', title='Balance', form=form, message='Incorrect PIN')
        return render_template('balance.html', title='Balance', form=form, bal=f'You have £{res[3]}')
    return render_template('balance.html', title='Balance', form=form)


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    con = sqlite3.connect("database/ATM_database.db")
    cur = con.cursor()
    form = MoneyWithdrawForm()
    if form.validate_on_submit():
        res = cur.execute(
            f"SELECT id, user_id, account_number, deposit, PIN FROM accounts WHERE account_number IS "
            f"'{form.account_number.data}'").fetchone()
        if not res:
            return render_template('deposit.html', title='Withdraw', form=form, message="Account doesn't exist")
        if form.password.data != str(res[4]):
            return render_template('deposit.html', title='Withdraw', form=form, message='Incorrect PIN')
        if int(res[3]) < int(form.money.data):
            return render_template('deposit.html', title='Withdraw', form=form, message='Not enough money')
        cur.execute(f"UPDATE accounts SET deposit='{int(res[3]) - int(form.money.data)}'")
        con.commit()
        return render_template('deposit.html', title='Withdraw', form=form, suc='SUCCESS')
    return render_template('deposit.html', title='Withdraw', form=form)


if __name__ == '__main__':
    app.run()
