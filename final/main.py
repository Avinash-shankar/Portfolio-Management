from flask import Flask, jsonify
import ast 
import json
import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import date
from datetime import timedelta
from yahoofinancials import YahooFinancials
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 8080
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'portfolio_management'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
 
mysql = MySQL(app)

@app.route("/<string:portfolio_id>")
def hello_world(portfolio_id):
    cursor = mysql.connection.cursor()
    std = cursor.execute(''' SELECT * FROM portfolio_performance WHERE portfolio_id = (%s)''',(portfolio_id))
    print(std)
    mysql.connection.commit()
    cursor.close()
    return 'success'


@app.route('/portfolio_performance/<string:test>')
def portfolio_measure(test):
    print(test)
    res = ast.literal_eval(test)
    print(test)
    res = json.loads(test)
    print(res)
    stocks = list(res.keys())
    weights = list(res.values())
    weights /= 100

    end = '2021-08-05'
    start = '2016-07-21'
    
    portfolio_ticker = []
    for stock in stocks:
        portfolio_ticker.append(stock+'.NS')

# Download the Data
    for stock_name, stock_ticker in zip(stocks, portfolio_ticker):
        yf = YahooFinancials(stock_ticker)
        data = yf.get_historical_price_data(start, end, 'daily')
        globals()[stock_name] = pd.DataFrame(data[stock_ticker]['prices'])
        globals()[stock_name] = globals()[stock_name].drop('date', axis=1).set_index('formatted_date')
        globals()[stock_name]['Date'] = pd.to_datetime(globals()[stock_name].index, format="%Y-%m-%d")
        globals()[stock_name].set_index('Date', drop=False, inplace=True)
        globals()[stock_name] = globals()[stock_name].dropna()

    closing_df = pd.DataFrame(index=stocks[0].index, columns=stocks)
    for stock in stocks:
        closing_df[stock] = globals()[stock]['adjclose']

# Download the NIFTY 50 data
    yf = YahooFinancials('^NSEI')
    data = yf.get_historical_price_data(start, end, 'daily')

    nifty_50 = pd.DataFrame(data['^NSEI']['prices'])
    nifty_50 = nifty_50.drop('date', axis=1).set_index('formatted_date')
    nifty_50['Date'] = pd.to_datetime(nifty_50.index, format="%Y-%m-%d")
    nifty_50.set_index('Date', drop=False, inplace=True)
    nifty_50 = nifty_50.dropna()
        
    nifty_50_daily = nifty_50['adjclose'].pct_change().dropna()

    daily_ret = closing_df.pct_change()
    daily_ret = daily_ret.dropna()

    corr_stock = daily_ret.copy()
    corr_stock['nifty_50'] = nifty_50_daily
    corr_df = corr_stock.corr(method='pearson')

    stock_beta = pd.Series(index=stocks)
    nifty_std = corr_stock['nifty_50'].std()
    for stock in stocks:
        stock_beta[stock] = (corr_df['nifty_50'][stock] * corr_stock[stock].std()) / nifty_std
    
    metrics = ['Return','Volatility','Sharpe Ratio', 'VaR', 'Portfolio Beta', 'Treynor Ratio', 'Jensen Alpha']
    results = np.zeros(7)

    daily_retn = daily_ret[stocks].copy()
    cov_matrixn = daily_retn.cov()
    stock_betan = stock_beta[stocks].copy()
    
    risk_free_rate = 0.0602
    alpha = 0.01
    days = 252
    market_return = nifty_50_daily.mean() * days 
    pb = 0
    
    portfolio_return = np.sum(daily_retn.mean()*weights) * days
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrixn, weights))) * np.sqrt(days)
    results[0] = portfolio_return
    results[1] = portfolio_std_dev

    # SHARPE RATIO => (portfolio_return - risk_free_rate) / volatility
    results[2] = (results[0] - risk_free_rate) / results[1]

    # VaR => return - (Z * volatility)
    results[3] = abs(portfolio_return - (portfolio_std_dev * norm.ppf(1 - alpha)))  # ppf => inverse of cdf

    for j in range(len(weights)):
        pb += weights[j] * stock_betan[j]

    # PORTFOLIO BETA => sum(weight * beta)
    results[4] = pb

    # TREYNOR RATIO => (portfolio_return - risk_free_rate) / portfolio_beta
    results[5] = (results[0] - risk_free_rate) / results[4]

    # JENSEN ALPHA => portfolio_return - (risk_free_rate + portfolio_beta * (market_return - risk_free_rate))
    results[6] = results[0] - (risk_free_rate + results[4] * (market_return - risk_free_rate))
    
    final_output = dict(zip(metrics, results))

    return jsonify(final_output)
    return test


if __name__ == "__main__":
    app.run(debug=True)