from flask import Flask, render_template, request, redirect
import requests

from bokeh.plotting import figure
from bokeh.embed import components

import pandas as pd

app = Flask(__name__)

app.vars={}

plot_choices = {
    'close': 'Close',
    'adj_close': 'Adj. Close',
    'open': 'Open',
    'adj_open': 'Adj. Open',
}

plot_colors = {
    0: 'blue',
    1: 'red',
    2: 'green',
    3: 'orange',
}

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
    
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"
    
    plot = figure(tools=TOOLS,
                  title='Data from Quandle WIKI set',
                  x_axis_label='date',
                  x_axis_type='datetime')
    
    # Remove the stock ticker so the options can be sorted
    del app.vars['stock_ticker']
    for i, key in enumerate(app.vars.keys()):
        plot.line(df['Date'], df[plot_choices[key]], legend='{0}: {1}'.format(stock_ticker,plot_choices[key]), color=plot_colors[i])
        
    script, div = components(plot)
    
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)
