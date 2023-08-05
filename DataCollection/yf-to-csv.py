# This python script takes as input the stock ticker, start and end date and pulls stock price history
# using yfinance. The date, close price and volume are stored in a csv file.
# Parameters: The ticker as a string and the start/end dates should be formatted as "YYYY-MM-DD"
# Example call of this script: python yf-to-csv.py "AAPL" "2017-01-01" "2017-04-30"

import yfinance as yf
import csv
import pandas as pd
import sys
def yftocsv(ticker, start, end):
    stock = yf.Ticker(ticker)
    stock.history(start=start, end=end).to_csv(f'yf-csv/{ticker}.csv', columns=['Close','Volume'])

if __name__ == "__main__":
    yftocsv(sys.argv[1], sys.argv[2], sys.argv[3])