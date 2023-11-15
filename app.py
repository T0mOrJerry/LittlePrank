from flask import Flask, render_template, redirect, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def starter():
    if request.method == 'POST':
        if request.form.get('action'):
            return redirect('/deposit')
        elif request.form.get('action') == 'withdraw':
            return redirect('/withdraw')
        elif request.form.get('action') == 'balance':
            return redirect('/balance')
    return render_template('main.html')


@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    return render_template('deposit.html')

if __name__ == '__main__':
    app.run()
