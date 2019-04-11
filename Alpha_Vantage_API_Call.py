#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Finviz_Screener_Scraper import scrape
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import numpy as np
import time
from tqdm import tqdm

tickers = scrape()
ts = TimeSeries(key='EK968A2XHRMFJY8J',output_format='pandas', indexing_type='date')


# In[2]:


def MACD(df):
    fast_len = 12
    slow_len = 26
    signal_len = 9
    macd = df['close'].ewm(span=fast_len).mean() - df['close'].ewm(span=slow_len).mean()
    signal = macd.ewm(span=signal_len).mean()
    indicator = macd - signal
    return indicator[-1]>indicator[-2]

#import talib
#macd, macdsignal, macdhist = talib.MACD(data['close'])

def KDJ(df,N=9,M1=3):
    llv_low = data['low'].rolling(N).min()
    hhv_high = data['high'].rolling(N).max()
    rsv = (df['close'] - llv_low)/(hhv_high - llv_low)
    k = rsv.ewm(adjust=False,alpha=1/M1).mean()
    d = k.ewm(adjust=False,alpha=1/M1).mean()
    j = 3*k-2*d
    today = (j-d)[-1]; yesterday = (j-d).shift(1)[-1]
    
    return today>0# and yesterday <0

def perc(df):
    short_avg = df['close'].rolling(window=3).mean()[-1]
    long_avg = df['close'].rolling(window=50).mean()[-1]
    
    return (short_avg - long_avg)/long_avg


# In[11]:


buy_list = {
    'symbol':[],
    'pass':[],
    'percentage':[],
    'price':[],
    'change':[]
}
for ticker in tqdm(tickers):
    data, meta_data = ts.get_daily(symbol=ticker, outputsize='compact')
    if data.shape[0]<100:
        pass
    data.columns = ['open','high','low','close','volume']
    
    time.sleep(12)
    
    buy_list['change'].append(str(round((data['close'][-1]-data['close'][-2])/data['close'][-2]*100,2))+'%')
    buy_list['symbol'].append(ticker)
    buy_list['pass'].append(KDJ(data)*MACD(data))
    buy_list['percentage'].append(perc(data))
    buy_list['price'].append(data['close'][-1])


# In[12]:


k = pd.DataFrame(buy_list)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
 
# create message object instance
msg = MIMEMultipart()
 

message = k[k['pass'] == True].sort_values(by=['percentage']).to_html()
 
# setup the parameters of the message
password = "stockscreener19"
msg['From'] = "ikushi.stockscreener@gmail.com"
msg['To'] = "xd.9440502@gmail.com"
msg['Subject'] = "{}_Screening_Complete".format(str(datetime.now())[:10].replace('-',''))
 
# add in the message body
msg.attach(MIMEText(message, 'html'))
 
#create server
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
 
#server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 

# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
#print "successfully sent email to %s:" % (msg['To'])


# In[ ]:




