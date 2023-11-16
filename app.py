from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Warwick-IFP'


class AccountForm(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()])
    password = StringField('Set PIN', validators=[DataRequired()])
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
    form = AccountForm()
    return render_template('signup.html', title='Account Creation', form=form)


if __name__ == '__main__':
    app.run()
