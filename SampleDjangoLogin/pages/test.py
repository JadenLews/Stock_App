#do a "pip install yfinance" in terminal

import yfinance as yf

# yf.Ticker( use the ticker symbol and it will return a yf object if it exists)
stock = yf.Ticker("AAPL")

# get daily stock data for the past month
stock_info = stock.history(period="1mo", interval="1d")
# returns a dataframe where you can specify a row with .iloc[ row num ]
#specify column with ['Open'],['Close'],['High'],['Low']

# swap out period with "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
# same with interval "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
print(stock.history(period="5d", interval='1h').iloc[0]["Open"])


# example view where it is given a string of the stock ticker, uses yf to get the stock object
# gets prices over time period, 

from django.utils.safestring import mark_safe
import json
from django.shortcuts import render
import yfinance as yf




def stock_details(request, symbol, time_frame='1mo'):
    stock = yf.Ticker(symbol)
    stock_info = stock.history(period=time_frame, interval="1d")
    
    # dates and closing prices
    dates = stock_info.index.strftime("%Y-%m-%d").tolist()
    closing_prices = stock_info['Close'].tolist()
    
    # Get company name from the stock info
    company_name = stock.info.get('shortName', 'N/A')  # 'N/A' if not available
    
    context = {
        'stock': {
            'symbol': symbol,
            'company_name': company_name,
            'price': round(stock_info['Close'].iloc[-1], 2), #latest closing price rounded 
        },
        'symbol': symbol,
        'time_frame': time_frame,
        'dates': mark_safe(json.dumps(dates)),
        'closing_prices': mark_safe(json.dumps(closing_prices)),
    }
    return render(request, 'pages/stock_details.html', context)