# source
# https://www.codingfinance.com/post/2018-04-03-calc-returns-py/

##############################################################################################################
# ░██████╗████████╗░█████╗░░█████╗░██╗░░██╗  ██████╗░███████╗████████╗██╗░░░██╗██████╗░███╗░░██╗░██████╗
# ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║░██╔╝  ██╔══██╗██╔════╝╚══██╔══╝██║░░░██║██╔══██╗████╗░██║██╔════╝
# ╚█████╗░░░░██║░░░██║░░██║██║░░╚═╝█████═╝░  ██████╔╝█████╗░░░░░██║░░░██║░░░██║██████╔╝██╔██╗██║╚█████╗░
# ░╚═══██╗░░░██║░░░██║░░██║██║░░██╗██╔═██╗░  ██╔══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔══██╗██║╚████║░╚═══██╗
# ██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░╚██╗  ██║░░██║███████╗░░░██║░░░╚██████╔╝██║░░██║██║░╚███║██████╔╝
# ╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝  ╚═╝░░╚═╝╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
##############################################################################################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web


##############################################################################################################
# Downloading the stock price for Netflix
netflix = web.get_data_yahoo("NFLX", 
                            start = "2009-01-01",
                            end = "2018-03-01")

print(netflix.head())


##############################################################################################################
# Next we will chart the Netflix’s adjusted closing price
netflix['Adj Close'].plot()
plt.xlabel("Date")
plt.ylabel("Adjusted")
plt.title("Netflix Price data")
plt.show()


##############################################################################################################
# Calculating the daily and monthly returns for individual stock
netflix_daily_returns = netflix['Adj Close'].pct_change() #percentage change
netflix_monthly_returns = netflix['Adj Close'].resample('M').ffill().pct_change()

# Looking at the head of the monthly returns
print(netflix_daily_returns.head())


##############################################################################################################
# Charting the daily and monthly for Netflix
##############################################################################################################
# Daily returns
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.plot(netflix_daily_returns)
ax1.set_xlabel("Date")
ax1.set_ylabel("Percent")
ax1.set_title("Netflix daily returns data")
plt.show()


# Monthly returns
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.plot(netflix_monthly_returns)
ax1.set_xlabel("Date")
ax1.set_ylabel("Percent")
ax1.set_title("Netflix monthly returns data")
plt.show()


##############################################################################################################
# To get a sense of how extreme the returns can be we can plot a histogram
##############################################################################################################
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
netflix_daily_returns.plot.hist(bins = 60)
ax1.set_xlabel("Daily returns %")
ax1.set_ylabel("Percent")
ax1.set_title("Netflix daily returns data")
ax1.text(-0.35,200,"Extreme Low\nreturns")
ax1.text(0.25,200,"Extreme High\nreturns")
plt.show()


##############################################################################################################
# Calculating the cumulative returns for the Netflix stock
##############################################################################################################
# To calculate the cumulative returns we will use the cumprod() function
netflix_cum_returns = (netflix_daily_returns + 1).cumprod()

# Next we can chart the cumulative returns of Netflix
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
netflix_cum_returns.plot()
ax1.set_xlabel("Date")
ax1.set_ylabel("Growth of $1 investment")
ax1.set_title("Netflix daily cumulative returns data")
plt.show()


# We can visualize that the monthly returns chart is much more smoother than the daily chart
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
netflix_cum_returns = (netflix_monthly_returns + 1).cumprod()
ax1.plot(netflix_cum_returns)
ax1.set_xlabel("Date")
ax1.set_ylabel("Growth of $1 investment")
ax1.set_title("Netflix Monthly cumulative returns data")
plt.show()



##############################################################################################################
# Multiple stocks
##############################################################################################################
# Downloading stock market data for multiple stocks
tickers = ["FB", "AMZN", "AAPL", "NFLX", "GOOG"]
multpl_stocks = web.get_data_yahoo(tickers,
                                    start = "2013-01-01",
                                    end = "2018-03-01")

# Charting the stock prices for multiple stocks
fig = plt.figure()
ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)
ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)
ax1.plot(multpl_stocks['Adj Close']['AMZN'])
ax1.set_title("Amazon")
ax2.plot(multpl_stocks['Adj Close']['AAPL'])
ax2.set_title("Apple")
ax3.plot(multpl_stocks['Adj Close']['FB'])
ax3.set_title("Facebook")
ax4.plot(multpl_stocks['Adj Close']['NFLX'])
ax4.set_title("Netflix")
ax5.plot(multpl_stocks['Adj Close']['GOOG'])
ax5.set_title("Google")
plt.tight_layout()
plt.show()


##############################################################################################################
# Calculating the returns for multiple stocks
##############################################################################################################
multpl_stock_daily_returns = multpl_stocks['Adj Close'].pct_change()
multpl_stock_monthly_returns = multpl_stocks['Adj Close'].resample('M').ffill().pct_change()

# Plot returns for multiple stocks
fig = plt.figure()
(multpl_stock_monthly_returns + 1).cumprod().plot()
plt.show()


##############################################################################################################
# Statistical Data - Calculating the Mean, standard deviation and other stats
##############################################################################################################
# Now we we will calculate the daily and monthly mean and standard deviations of the returns. 
# We will use mean() and std() functions for our purpose.
print(f"\n The mean monthly returns are: ")
print(multpl_stock_monthly_returns.mean())

print(f"\n The monthly standard deviation of returns are: ")
print(multpl_stock_monthly_returns.std())


##############################################################################################################
# Calculating the correlation and covariance using pandas
##############################################################################################################
# Correlation
print(multpl_stock_monthly_returns.corr())

# Covariance
print(multpl_stock_monthly_returns.cov())
