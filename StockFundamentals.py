# source
# https://towardsdatascience.com/discounted-cash-flow-with-python-f5103921942e
# https://medium.com/@polanitzer/building-a-dcf-valuation-in-python-step-by-step-9ba686e0b3a
# https://www.reddit.com/r/fintech/comments/nk6ryl/automated_dcf_calculator_using_yahoo_finance/
# https://github.com/Jarrlist/yahoo
# https://algotrading101.com/learn/yahoo-finance-api-guide/
# https://algotrading101.com/learn/yfinance-guide/
# https://fsymbols.com/generators/tarty/

# ##############################################################################################################
# ░██████╗████████╗░█████╗░░█████╗░██╗░░██╗
# ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║░██╔╝
# ╚█████╗░░░░██║░░░██║░░██║██║░░╚═╝█████═╝░
# ░╚═══██╗░░░██║░░░██║░░██║██║░░██╗██╔═██╗░
# ██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░╚██╗
# ╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝

# ███████╗██╗░░░██╗███╗░░██╗██████╗░░█████╗░███╗░░░███╗███████╗███╗░░██╗████████╗░█████╗░██╗░░░░░░██████╗
# ██╔════╝██║░░░██║████╗░██║██╔══██╗██╔══██╗████╗░████║██╔════╝████╗░██║╚══██╔══╝██╔══██╗██║░░░░░██╔════╝
# █████╗░░██║░░░██║██╔██╗██║██║░░██║███████║██╔████╔██║█████╗░░██╔██╗██║░░░██║░░░███████║██║░░░░░╚█████╗░
# ██╔══╝░░██║░░░██║██║╚████║██║░░██║██╔══██║██║╚██╔╝██║██╔══╝░░██║╚████║░░░██║░░░██╔══██║██║░░░░░░╚═══██╗
# ██║░░░░░╚██████╔╝██║░╚███║██████╔╝██║░░██║██║░╚═╝░██║███████╗██║░╚███║░░░██║░░░██║░░██║███████╗██████╔╝
# ╚═╝░░░░░░╚═════╝░╚═╝░░╚══╝╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═════╝░
##############################################################################################################

# yfinance is a popular open source library developed by Ran Aroussi.
# https://pypi.org/project/yfinance/

# import yfinance as yf
# msft = yf.Ticker("MSFT")
# print(msft.info)

# balancesheet = msft.balance_sheet
# print(balancesheet)

##############################################################################################################
# Library Layout
##############################################################################################################
# The layout itself is also really simple, there are just three modules:
#     yf.Tickers
#     yf.download
#     yf.pandas_datareader

import yfinance as yf

# yfinance.Ticker object <AAPL>
aapl= yf.Ticker("aapl")
print(aapl)

# download historical data using the yfinance library 
# (interval: data interval (1m data is only for available for last 7 days, and data interval <1d for the last 60 days)
aapl_historical = aapl.history(start="2022-09-25", end="2022-09-30", interval="1m")
print(aapl_historical)

# multiple tickers (Note that the default with no interval specified is daily data)
data = yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
print(data)

# if we want to group by ticker instead of Open/High/Low/Close we can do:
data = yf.download("AMZN AAPL GOOG", start="2017-01-01",
                    end="2017-04-30", group_by='tickers')
print(data)

##############################################################################################################
# Fundamentals download with yFinance
##############################################################################################################

##############################################################################################################
# Price to Earnings Ratio
# with the Ticker.info() method
aapl = yf.Ticker("aapl")
aapl.info['forwardPE']
print(f"PE ratio of {aapl.info['symbol']} : ")
print(aapl.info['forwardPE'])

##############################################################################################################
# Dividends
aapl.info['dividendRate']
print(f"Yearly dividend rate of {aapl.info['symbol']} : ")
print(aapl.info['dividendRate'])

# breakdown of each dividend payout as it occurred and on what date, you can use Ticker.dividends():
aapl.dividends
print(aapl.dividends)

##############################################################################################################
# Fundamentals data with multiple tickers at once
##############################################################################################################

##############################################################################################################
import pandas as pd

tickers_list = ["aapl", "goog", "amzn", "BAC", "BA"] # example list
tickers_data= {} # empty dictionary
print(tickers_list)

##############################################################################################################
# We then loop through the list of the tickers, in each case adding to our dictionary a key, value pair where the key is the ticker 
# and the value the dataframe returned by the info() method for that ticker:
for ticker in tickers_list:
    ticker_object = yf.Ticker(ticker)

    #convert info() output from dictionary to dataframe
    temp = pd.DataFrame.from_dict(ticker_object.info, orient="index")
    temp.reset_index(inplace=True)
    temp.columns = ["Attribute", "Recent"]
    
    # add (ticker, dataframe) to main dictionary
    tickers_data[ticker] = temp

tickers_data
print(tickers_data)

##############################################################################################################
# We then combine this dictionary of dataframes into a single dataframe: 
combined_data = pd.concat(tickers_data)
combined_data = combined_data.reset_index()
combined_data
print(combined_data)

##############################################################################################################
# And then delete the unnecessary “level_1” column and clean up the column names:
del combined_data["level_1"] # clean up unnecessary column
combined_data.columns = ["Ticker", "Attribute", "Recent"] # update column names

combined_data
print(combined_data)

##############################################################################################################
# Comparing by a particular attribute
##############################################################################################################

# It’s quite easy actually, lets try for one of the attributes in info()– the fullTimeEmployees count:
employees = combined_data[combined_data["Attribute"]=="fullTimeEmployees"].reset_index()
del employees["index"] # clean up unnecessary column

employees
print(employees)

# So now we have a dataframe of just the employee counts- one entry per ticker- and we can now order by the ‘Recent’ column:
employees_sorted = employees.sort_values('Recent',ascending=False)
employees_sorted
print(employees_sorted)

# ##############################################################################################################
# download trading data using the yfinance library
##############################################################################################################

# Market Cap
aapl.info["marketCap"]
print(aapl.info["marketCap"])

# Volume
aapl.info["volume"]
print(aapl.info["volume"])

# If you want the average volume over the last 24 hours do:
aapl.info["averageVolume"]
print(aapl.info["averageVolume"])

# And finally if you want the average volume over the last 10 days:
aapl.info["averageVolume10days"]
print(aapl.info["averageVolume10days"])

##############################################################################################################
# Highs and Lows
##############################################################################################################
# Remember, you can find the highs and lows for any time interval: “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
aapl_historical = aapl.history(period="max", interval="1wk")
aapl_historical
print(aapl_historical) # Wow, almost 40 years of data!

# Just filter the dataframe with:
aapl_historical["High"]
aapl_historical["Low"]
# Alternatively, you can use info() to get the following useful high/low information:
# dayHigh
# dayLow
# fiftyTwoWeekHigh
# fiftyTwoWeekLow
aapl.info["fiftyTwoWeekHigh"]
print(aapl.info["fiftyTwoWeekHigh"])

##############################################################################################################
# download options data using the yfinance library
##############################################################################################################
# To download options data we can use the option_chain() method. It takes the parameter as input:
#    date: (YYYY-MM-DD), expiry date. If None return all options data.
# And has the opt.calls and opt.puts methods.

##############################################################################################################
# How do I get Expiration dates?
aapl.options
print(aapl.options)

##############################################################################################################
# How do I get Calls Data?
# get option chain calls data for specific expiration date
opt = aapl.option_chain(date='2023-01-20')
opt.calls
print(opt.calls)

##############################################################################################################
# How do I get Puts Data?
opt.puts
print(opt.puts)

##############################################################################################################
# Finally, opts by itself returns a ticker object containing both the calls and puts data together, if that’s useful to you!
opt

