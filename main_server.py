import scipy.io
from flask import Flask, render_template, request

from helpers.model_helper import get_result

app = Flask(__name__)

res = []

@app.route('/')
def init():
    global res
    res = []
    return render_template('chatpage.html', result = res)

@app.route('/', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
       msg = request.form['Msg']
       global res
       if len(msg) > 0:
           res.append(['human', msg])
           res.append(['bot', get_result(msg)])
       return render_template("chatpage.html", result = res)

if __name__ == '__main__':
   app.run(debug = True)