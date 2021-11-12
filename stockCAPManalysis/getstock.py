# let's get some 1 minute bar data using alphavantage.co
# register for an APIKEY at alphavantage.co
# NOTE: you must set outputsize = full in your url otherwise you get truncated data
# SOURCE: https://www.alphavantage.co/

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import io
import requests
import os

# TODO: replace with your own API key


# get daily stock prices
def getMonthlyStockPrices(symbol, apikey):
    if(symbol=='^GSPC'):
        path = '../Data/stocks_monthly/' + symbol + '_Stock.csv'
        print('LocalData:')
        with open(path, mode='r', encoding='utf-8') as f:
            df = pd.read_csv(f)
            NEW_timeStamp = pd.to_datetime(df['timestamp'])
            df.index = NEW_timeStamp
            df = df.drop(columns = {'timestamp'})
            return df
    ts = TimeSeries( key=apikey )
    data, meta_data = ts.get_monthly_adjusted( symbol )
    symbol_df = pd.DataFrame.from_dict( data, orient = 'index' )
    symbol_df = symbol_df.apply(pd.to_numeric)
    symbol_df.index = pd.to_datetime( symbol_df.index )
    symbol_df.columns = [ 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amt']
    symbol_df = symbol_df.sort_index( ascending=True )
    return symbol_df

# get daily stock prices
def getDailyStockPrices(symbol, apikey):
    '''
    path = '../Data/Stocks/' + symbol + '_Stock_Full.csv'
    if os.path.exists(path):
        print('LocalData:')
        with open(path, mode='r', encoding='utf-8') as f:
            df = pd.read_csv(f)
            NEW_timeStamp = pd.to_datetime(df['timestamp'])
            df.index = NEW_timeStamp
            df = df.drop(columns = {'timestamp'})
            return df
    else:
        print('DownloadData:')
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol=' + 'symbol_replace' + '&apikey=' + apikey + '&datatype=csv'
        url = url.replace('symbol_replace', symbol)
        # what we got
        s = requests.get(url).content
        # stock is Dataframe type
        stock = pd.read_csv(io.StringIO(s.decode('utf-8')))
        NEW_timeStamp = pd.to_datetime(stock['timestamp'])
        stock.index = NEW_timeStamp
        stock = stock.drop(columns = {'timestamp'})
        # check path
        if not os.path.exists(path[0:15]):
            os.makedirs(path[0:15])
        stock.to_csv(path)
        return stock
    return None
    '''
    ts = TimeSeries( key=apikey ) # json字典（默认）
    # 得到天为间隔的数据
    data, meta_data = ts.get_daily_adjusted( symbol, outputsize='full' )
    # data: dict类型数据, orient: 把字典的键作为列就是columns, 作为index(行)就是index
    # 转化为dataframe数据类型
    symbol_df = pd.DataFrame.from_dict( data, orient = 'index' )
    # 对每个数据使用pd.to_numeric, 转化成数值
    # s = pd.Series(['1.0', '2', -3])
    # pd.to_numeric(s)
    #     0    1.0
    #     1    2.0
    #     2   -3.0
    #     dtype: float64
    symbol_df = symbol_df.apply(pd.to_numeric)
    # 把index转化成时间类型并返回新的index覆盖原来的
    symbol_df.index = pd.to_datetime( symbol_df.index )
    # 改列名
    symbol_df.columns = [ 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amt', 'split_coef' ]
    # 按index, 即时间顺序升序排列
    symbol_df = symbol_df.sort_index( ascending=True )
    # 返回得到并经过处理的数据
    return symbol_df

# get minute stock prices
def getMinuteStockPrices(symbol, apikey):
    ts = TimeSeries( key=apikey )
    data, meta_data = ts.get_intraday( symbol, interval='1min', outputsize='full' )
    symbol_df = pd.DataFrame.from_dict( data, orient = 'index' )
    symbol_df = symbol_df.apply(pd.to_numeric)
    symbol_df.index = pd.to_datetime( symbol_df.index )
    symbol_df.columns = [ 'open', 'high', 'low', 'close', 'volume' ]
    symbol_df = symbol_df.sort_index( ascending=True )
    return symbol_df


# get minute stock prices
def getLatestStockPrice(symbol):
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + symbol + '&apikey=' + apikey + '&datatype=csv'
    s = requests.get(url).content
    symbol_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    return symbol_df['price'].values[0]
