#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 1. Predict weights for model 1 & 2 by maximising Sharpe Ratio
# 2. Plot return: portfolio early vs portfolio ml vs nifty


# In[2]:


import numpy as np
import pandas as pd
from scipy.stats import norm

import plotly.express as px

import tensorflow as tf
from tensorflow.keras.layers import LSTM, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
import tensorflow.keras.backend as K

from datetime import date
from datetime import timedelta

from yahoofinancials import YahooFinancials

import warnings
warnings.filterwarnings('ignore')


# In[3]:


end = '2021-08-04'
start = '2016-07-21'


# In[4]:


weight_df = pd.read_csv('../data/WeightsDF.csv')
weight_df.set_index('Portfolio', inplace=True)


# In[5]:


stocks = np.array(weight_df.columns).tolist()

i1 = 0
i2 = 1
portfolio1 = []
portfolio2 = []
for stock in stocks:
    if weight_df[stock][i1] > 0:
        portfolio1.append(stock)
    if weight_df[stock][i2] > 0:
        portfolio2.append(stock)


# In[6]:


portfolio_ticker = []
for stock in stocks:
    portfolio_ticker.append(stock+'.NS')


# In[7]:


for stock_name, stock_ticker in zip(stocks, portfolio_ticker):
    
    yf = YahooFinancials(stock_ticker)
    data = yf.get_historical_price_data(start, end, 'daily')
    globals()[stock_name] = pd.DataFrame(data[stock_ticker]['prices'])
    globals()[stock_name] = globals()[stock_name].drop('date', axis=1).set_index('formatted_date')

    globals()[stock_name]['Date'] = pd.to_datetime(globals()[stock_name].index, format="%Y-%m-%d")
    globals()[stock_name].set_index('Date', drop=False, inplace=True)

    globals()[stock_name] = globals()[stock_name].dropna()


# In[8]:


closing_df = pd.DataFrame(index=IRCTC.index, columns=stocks)
for stock in stocks:
    closing_df[stock] = globals()[stock]['adjclose']


# In[9]:


closing_df


# In[10]:


portfolio = []

portfolio.append(portfolio1)
portfolio.append(portfolio2)

portfolio


# In[11]:


yf = YahooFinancials('^NSEI')

data = yf.get_historical_price_data(start, end, 'daily')

nifty_50 = pd.DataFrame(data['^NSEI']['prices'])
nifty_50 = nifty_50.drop('date', axis=1).set_index('formatted_date')

nifty_50['Date'] = pd.to_datetime(nifty_50.index, format="%Y-%m-%d")
nifty_50.set_index('Date', drop=False, inplace=True)

nifty_50 = nifty_50.dropna()
    
nifty_50_daily = nifty_50['adjclose'].pct_change().dropna()


# In[12]:


daily_ret = closing_df.pct_change()
daily_ret = daily_ret.dropna()

corr_stock = daily_ret.copy()
corr_stock['nifty_50'] = nifty_50_daily

corr_df = corr_stock.corr(method='pearson')


# In[13]:


# Beta => Covariance / Variance    OR    (Correlation * Stock_STD) / StandardMarket_STD

stock_beta = pd.Series(index=stocks)
nifty_std = corr_stock['nifty_50'].std()

for stock in stocks:
    stock_beta[stock] = (corr_df['nifty_50'][stock] * corr_stock[stock].std()) / nifty_std


# In[14]:


metrics = ['Return','Volatility','Sharpe Ratio', 'VaR', 'Portfolio Beta', 'Treynor Ratio', 'Jensen Alpha']
metrics_df = pd.DataFrame(columns=metrics)

weight_df = pd.DataFrame(columns=stocks)


# In[15]:


risk_free_rate = 0.0602
alpha = 0.01
days = 252
market_return = nifty_50_daily.mean() * days 


# In[16]:


for portfolios in portfolio:
    
    cd = closing_df[portfolios].copy()
    
    data_w_ret = np.concatenate([cd.values[1:], cd.pct_change().values[1:]], axis=1)  
    
    outputs = len(cd.columns)
    
    def sharpe_loss(_,y_pred):
    
        coeffs = tf.tile(y_pred, (cd.shape[0], 1))
        portfolio_values = tf.reduce_sum(tf.multiply(coeffs, cd), axis=1)

        portfolio_returns = (portfolio_values[1:] - portfolio_values[:-1]) / portfolio_values[:-1]

        sharpe = K.mean(portfolio_returns) / K.std(portfolio_returns)

        # exp keeps relative ordering between positives and negatives
        # since we want to maximize sharp, while gradient descent minimizes the loss
        # we negate the Sharpe value
        return K.exp(-sharpe)
    
    
    model = Sequential([LSTM(units=64, input_shape=data_w_ret.shape), Flatten(), Dense(outputs, activation='softmax')])
    model.compile(loss=sharpe_loss, optimizer="adam", metrics=['accuracy'])    
    
    fit_predict_data = data_w_ret[np.newaxis,:]        
    model.fit(fit_predict_data, np.zeros((1, outputs)), epochs=250, shuffle=False)
    
    weight_1 = model.predict(fit_predict_data)[0]
    weight_1 = pd.Series(weight_1, index=portfolios)
    
    
    cd = pd.DataFrame(index=IRCTC.index, columns=portfolios)
    for stock in portfolios:
        cd[stock] = globals()[stock]['adjclose']
    
    tdf = cd.copy().pct_change()
    tdf.drop([tdf.index[0]], inplace=True)
    tcs = tdf.copy()
    tcs['NIFTY'] = nifty_50_daily
    tcsdf = tcs.corr(method='pearson')

    r1 = np.zeros(len(metrics))
    sb1 = stock_beta[portfolios]
    pb1 = 0
    twl1 = np.array(list(weight_1.values))
    tcovdf1 = tdf.cov()

    pr1 = np.sum(tdf.mean() * twl1) * days
    pstd1 = np.sqrt(np.dot(twl1.T,np.dot(tcovdf1, twl1))) * np.sqrt(days)

    r1[0] = pr1
    r1[1] = pstd1

    # SHARPE RATIO => (portfolio_return - risk_free_rate) / volatility
    r1[2] = (r1[0] - risk_free_rate) / r1[1]

    # VaR => return - (Z * volatility)
    r1[3] = abs(pr1 - (pstd1 * norm.ppf(1 - alpha)))

    # PORTFOLIO BETA => sum(weight * beta)
    for j in range(len(twl1)):
        pb1 += twl1[j] * sb1[j]
    r1[4] = pb1

    # TREYNOR RATIO => (portfolio_return - risk_free_rate) / portfolio_beta
    r1[5] = (r1[0] - risk_free_rate) / r1[4]

    # JENSEN ALPHA => portfolio_return - (risk_free_rate + portfolio_beta * (market_return - risk_free_rate))
    r1[6] = r1[0] - (risk_free_rate + r1[4] * (market_return - risk_free_rate))   

    r1 = pd.Series(r1, index=metrics)
    
    metrics_df = metrics_df.append(r1, ignore_index=True)
    
    weight_df = weight_df.append(weight_1, ignore_index=True)


# In[17]:


mcw = pd.read_csv('../data/mcw.csv')
mcm = pd.read_csv('../data/mcm.csv')


# In[18]:


mcm


# In[19]:


metrics_df


# In[20]:


mcw


# In[21]:


weight_df


# In[22]:


mcw_1 = mcw.iloc[0][1:]
mcw_1 = mcw_1.dropna().values

mcw_2 = mcw.iloc[1][1:]
mcw_2 = mcw_2.dropna().values

weight_1 = weight_df.iloc[0].dropna().values
weight_2 = weight_df.iloc[1].dropna().values


# In[23]:


df1 = closing_df.copy()


# In[24]:


df_daily_returns = df1.pct_change()

df_daily_returns = df_daily_returns[1:]

df_cum_daily_returns = (1 + df_daily_returns).cumprod() - 1


# In[25]:


port_returns_1 = pd.DataFrame(index=df_cum_daily_returns.index, columns=['Monte Carlo', 'DL', 'Dynamic DL'])
port_returns_2 = pd.DataFrame(index=df_cum_daily_returns.index, columns=['Monte Carlo', 'DL', 'Dynamic DL'])


# In[26]:


for i in range(len(df_cum_daily_returns)):
    
    port_returns_1.iloc[i]['Monte Carlo'] = np.sum(df_cum_daily_returns[portfolio1].iloc[i].values * mcw_1)
    port_returns_1.iloc[i]['DL'] = np.sum(df_cum_daily_returns[portfolio1].iloc[i].values * weight_1)
    

for i in range (len(closing_df)-1):
    
    v = np.concatenate([[closing_df[portfolio1].iloc[i].values], [df_daily_returns[portfolio1].iloc[i].values]], axis=1)
    v = v[np.newaxis,:] 
    qqq = model.predict(v)[0]
    
    port_returns_1.iloc[i]['Dynamic DL'] = np.sum(df_cum_daily_returns[portfolio1].iloc[i].values * qqq)


# In[27]:


for i in range(len(df_cum_daily_returns)):
    
    port_returns_2.iloc[i]['Monte Carlo'] = np.sum(df_cum_daily_returns[portfolio2].iloc[i].values * mcw_2)
    port_returns_2.iloc[i]['DL'] = np.sum(df_cum_daily_returns[portfolio2].iloc[i].values * weight_2)
    

for i in range (len(closing_df)-1):
    
    v = np.concatenate([[closing_df[portfolio2].iloc[i].values], [df_daily_returns[portfolio2].iloc[i].values]], axis=1)
    v = v[np.newaxis,:] 
    qqq = model.predict(v)[0]
    
    port_returns_2.iloc[i]['Dynamic DL'] = np.sum(df_cum_daily_returns[portfolio2].iloc[i].values * qqq)


# In[28]:


port_returns_1 *= 252
port_returns_2 *= 252


# In[29]:


port_returns_1


# In[30]:


port_returns_2


# In[31]:


fig1 = px.line(port_returns_1, x=port_returns_1.index, y=['Monte Carlo', 'DL', 'Dynamic DL'])

fig1.update_layout(
    title="Portfolio Returns over Time",
    xaxis_title="Date",
    yaxis_title="Returns",
    legend_title="Returns",
)

fig1.show()


# In[32]:


fig2 = px.line(port_returns_2, x=port_returns_2.index, y=['Monte Carlo', 'DL', 'Dynamic DL'])

fig2.update_layout(
    title="Portfolio Returns over Time",
    xaxis_title="Date",
    yaxis_title="Returns",
    legend_title="Returns",
)

fig2.show()


# In[33]:


port_returns_1.to_csv('../data/port1.csv')
port_returns_2.to_csv('../data/port2.csv')


# In[34]:


fig1.write_image('../img/portfolio1.png')
fig2.write_image('../img/portfolio2.png')


# In[ ]:




