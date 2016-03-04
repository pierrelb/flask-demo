from flask import Flask, render_template, request, redirect
import requests

import pandas as pd

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
    # Get the stock ticker from the dictionary
    stock_ticker = app.vars['stock_ticker']
    
    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock_ticker
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    rel_data = raw_data.json()
    df = pd.DataFrame(data=rel_data['data'],columns=rel_data['column_names'])
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df = df.sort_values(by='Date',ascending=False)
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(host='0.0.0.0')#port=33507)
