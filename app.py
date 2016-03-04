from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

app.vars={}
@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        for key in request.form.keys():
            app.vars[key] = request.form[key]
        return redirect('/graph')

@app.route('/graph')
def graph():
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(host='0.0.0.0')#port=33507)
