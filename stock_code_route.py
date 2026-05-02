import threading
import itertools
import time
import sys
import yfinance as yf
from datetime import date
import time
import sys


#Program starts here

#Nifty stocks
#symbols=["RELIANCE.NS","LT.NS","TORNTPHARM.NS","HEROMOTOCO.NS","TATACONSUM.NS","PGHH.NS","GODREJCP.NS","TECHM.NS","DMART.NS","ABBOTINDIA.NS","HDFCBANK.NS","ALKEM.NS","ASIANPAINT.NS","AUROPHARMA.NS","MARUTI.NS","TCS.NS","TATASTEEL.NS","BHARTIARTL.NS","ITC.NS","KOTAKBANK.NS","CIPLA.NS","BRITANNIA.NS","ULTRACEMCO.NS","INDUSINDBK.NS","HDFCLIFE.NS","WIPRO.NS","BAJAJ-AUTO.NS","SHREECEM.NS","TITAN.NS","HINDUNILVR.NS","HINDALCO.NS","ICICIBANK.NS","BAJFINANCE.NS","NESTLEIND.NS","GRASIM.NS","PIDILITIND.NS","HCLTECH.NS","EICHERMOT.NS","INFY.NS","MARICO.NS","SUNPHARMA.NS","BANDHANBNK.NS","SBIN.NS"]

#Nifty Next 50
#symbols=['ACC.NS','ADANIENT.NS','ADANIGREEN.NS','AMBUJACEM.NS','DMART.NS','BAJAJHLDNG.NS','BANDHANBNK.NS','BANKBARODA.NS','BERGEPAINT.NS','BIOCON.NS','BOSCHLTD.NS','CHOLAFIN.NS','COLPAL.NS','DLF.NS','DABUR.NS','NYKAA.NS','GAIL.NS','GLAND.NS','GODREJCP.NS','HDFCAMC.NS','HAVELLS.NS','ICICIGI.NS','ICICIPRULI.NS','IOC.NS','INDUSTOWER.NS','NAUKRI.NS','INDIGO.NS','JUBLFOOD.NS','LICI.NS','LUPIN.NS','MARICO.NS','MUTHOOTFIN.NS','PAYTM.NS','PIIND.NS','PIDILITIND.NS','PGHH.NS','PNB.NS','SBICARD.NS','SRF.NS','SIEMENS.NS','SAIL.NS','TATAPOWER.NS','TORNTPHARM.NS','MCDOWELL-N.NS','VEDL.NS','ETERNAL.NS','ZYDUSLIFE.NS'] 

#Best stocks
#symbols=["AUBANK.NS","DIVISLAB.NS","ASTEC.NS","HEIDELBERG.NS","ADVENZYMES.NS","DEEPAKNTR.NS","ASTRAL.NS","MPHASIS.NS","AMARAJABAT.NS","JSWSTEEL.NS","NAVINFLUOR.NS","GALAXYSURF.NS","ICICIGI.NS","HDFCLIFE.NS","TATAELXSI.NS","CARBORUNIV.NS","PERSISTENT.NS","ENDURANCE.NS","HDFC.NS","HDFCBANK.NS","ASIANPAINT.NS","IGL.NS","BANDHANBNK.NS","BALAMINES.NS","BAJFINANCE.NS","SUPREMEIND.NS","LAURUSLABS.NS","POLYCAB.NS","BHARTIARTL.NS","SUMICHEM.NS","VOLTAS.NS","CIPLA.NS","TCS.NS","DRREDDY.NS","EICHERMOT.NS","SUNPHARMA.NS","BRITANNIA.NS","RELIANCE.NS","SBIN.NS"]

#nifty midcap 50 stocks 
#symbols =  ['APLAPOLLO.NS','AUBANK.NS','ASHOKLEY.NS','AUROPHARMA.NS','BSE.NS','BHARATFORG.NS','BHEL.NS','COFORGE.NS','COLPAL.NS','CUMMINSIND.NS','DABUR.NS','DIXON.NS','FEDERALBNK.NS','FORTIS.NS','GMRAIRPORT.NS','GODREJPROP.NS','HDFCAMC.NS','HEROMOTOCO.NS','HINDPETRO.NS','IDFCFIRSTB.NS','IRCTC.NS','INDUSTOWER.NS','INDUSINDBK.NS','JUBLFOOD.NS','LUPIN.NS','MANKIND.NS','MARICO.NS','MFSL.NS','MPHASIS.NS','MUTHOOTFIN.NS','NHPC.NS','NMDC.NS','OBEROIRLTY.NS','OIL.NS','PAYTM.NS','OFSS.NS','POLICYBZR.NS','PIIND.NS','PAGEIND.NS','PERSISTENT.NS','PHOENIXLTD.NS','POLYCAB.NS','PRESTIGE.NS','SBICARD.NS','SRF.NS','SUPREMEIND.NS','SUZLON.NS','TIINDIA.NS','UPL.NS','YESBANK.NS','ZEEL.NS']

#MY
symbols = ['CRISIL.NS','BALRAMCHIN.NS','KPRMILL.NS','WAAREEENER.NS','GRAVITA.NS','ECLERX.NS','TCIEXP.NS','COROMANDEL.NS','BOROLTD.NS','GROWW.NS','AVANTIFEED.NS','PIIND.NS','INDUSTOWER.NS','IRCTC.NS','ICICIAMC.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','APLAPOLLO.NS','PVRINOX.NS','VBL.NS','UNITDSPR.NS','SOLARINDS.NS','PFC.NS','NAVINFLUOR.NS','PIDILITIND.NS','MAZDOCK.NS','LICI.NS','INDHOTEL.NS','IRFC.NS','BLUESTARCO.NS','HAVELLS.NS','HINDZINC.NS','DMART.NS','ADANIPOWER.NS','ADANIENSOL.NS','SBIN.NS','HINDALCO.NS','INDIGO.NS','LT.NS','RELIANCE.NS','ONGC.NS','SBILIFE.NS','TCS.NS','BAJFINANCE.NS','SUNPHARMA.NS','MARUTI.NS','BHARTIARTL.NS','BAJAJ-AUTO.NS','ASIANPAINT.NS','HDFCBANK.NS','BEL.NS','ADANIPORTS.NS','CONCOR.NS','LODHA.NS','KALYANKJIL.NS','PETRONET.NS','JSWSTEEL.NS','AUBANK.NS','ULTRACEMCO.NS','ABB.NS','SPLPETRO.NS','SUPREMEIND.NS','FLUOROCHEM.NS','APOLLOTYRE.NS','SRF.NS','SUMICHEM.NS','APOLLOHOSP.NS','MOTHERSON.NS','HINDCOPPER.NS','POLYCAB.NS']
#symbols = ['SBIN.NS']

ma_stocks50=[]
ma_stocks200=[]
rsi_stocks=[]
most_eligible_stocks=[]
stocks_in_uptrend=[]


def calculate_ema(prices, period):
    k = 2 / (period + 1)
    ema = prices[0]  # start with first price
    for price in prices[1:]:
        ema = price * k + ema * (1 - k)
    return round(ema, 2)


def isElgible(ticker, moving_average,cur_price):
    difference = abs(cur_price - moving_average)
    percent_difference = (difference / moving_average) * 100
    if percent_difference <= 2:
        return True
    return False


def last_rsi(prices, period=14):
    gains = []
    losses = []

    # Initial average gain & loss
    for i in range(1, period + 1):
        change = prices[i] - prices[i - 1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    # Wilder smoothing
    for i in range(period + 1, len(prices)):
        change = prices[i] - prices[i - 1]
        gain = max(change, 0)
        loss = max(-change, 0)

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return round(rsi, 2)

def eligibleRsi(ticker, rsi)->bool:
    if rsi <= 35 or rsi >=65:
        rsi_stocks.append(ticker+"-"+str(rsi))
        return True
    return False

def is_in_uptrend(ticker, prices, ema_50, ema_200):
    """
    Detects if a stock is in an uptrend based on price list (past to current order).
    Returns True if stock is in uptrend, False otherwise.
    
    Uptrend criteria:
    1. Current price > 50-day EMA
    2. 50-day EMA > 200-day EMA
    3. Recent prices above 50-day EMA (confirmation)
    """
    if len(prices) < 200:
        return False
    current_price = prices[-1]
    #print(ema_50, ema_200,current_price,ticker)
    
    # Primary uptrend condition: Price > 200 EMA
    if current_price > ema_200 and ema_50 > ema_200:
        # Confirmation: Check if at least 60% of recent 50 prices are above 50 EMA
        recent_50 = prices[-50:]
        nick=0
        len_of_prices = len(prices)
        ema_50_calculated = []
        while nick<50:
            ema_50_calculated.append(calculate_ema(prices[:len_of_prices-nick], 50))
            nick=nick+1
        ema_50_calculated.reverse()
        
        above_ema_count = sum(1 for index in range(0,49) if recent_50[index] > ema_50_calculated[index] and ema_50_calculated[index] > ema_200)
        if above_ema_count >= 30:  # 60% of 50 = 30
            stocks_in_uptrend.append(ticker)
            return True 
    return False
    
def print_call():
    final_obj = {}
    final_obj['Date_of_Analysis'] = str(date.today())
    stock_data = []
    
    stock_data.append({
        'title':'stocks near 50 day Moving Average',
        'data':list(set(ma_stocks50))
    })

    stock_data.append({
        'title':'stocks near 200 day Moving Average',
        'data':list(set(ma_stocks200))
    })

    stock_data.append({
        'title':'stocks at RSI Buy',
        'data':list(set(rsi_stocks))
    })

    stock_data.append({
        'title':'stocks in Uptrend',
        'data':list(set(stocks_in_uptrend))
    })

    stock_data.append({
        'title':'most_eligible_stocks',
        'data':list(set(most_eligible_stocks))
    })
    
    final_obj['Stock_Data'] = stock_data
    return final_obj
 
def program():
    for symb in symbols:
        closing_prices=[]
        ticker = yf.Ticker(symb)
        hist = ticker.history(period='300d')
        closing_prices = hist["Close"].tail(250).tolist()
        closing_prices = [round(price, 2) for price in closing_prices]
        if len(closing_prices)<50:
           continue
        
        ema_50 = calculate_ema(closing_prices, 50) #50 day ma
        #print(ema_50)
        if(isElgible(symb, ema_50, closing_prices[-1])):
            ma_stocks50.append(symb)
        rsi = last_rsi(closing_prices, 14)
        is_eligible_rsi = eligibleRsi(symb, rsi)
        #print(rsi)
        if(len(closing_prices)>200):
            ema_200 = calculate_ema(closing_prices, 200) #200 day ma
            #print(ema_200)
            if(isElgible(symb, ema_200, closing_prices[-1])):
                ma_stocks200.append(symb)
            if is_in_uptrend(symb, closing_prices, ema_50, ema_200):
                stocks_in_uptrend.append(symb)
            if ((symb in ma_stocks50 or symb in ma_stocks200) and symb in stocks_in_uptrend) or (is_eligible_rsi and symb in ma_stocks200):
                most_eligible_stocks.append(symb)
    
    result = print_call()
    return result
