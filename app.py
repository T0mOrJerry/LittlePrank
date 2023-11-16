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
    return render_template('deposit.html', title='Deposit')


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
        return redirect('/success')
    return render_template('signup.html', title='Account Creation', form=form)


@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html', title='Deposit', account_num=n)


if __name__ == '__main__':
    app.run()
