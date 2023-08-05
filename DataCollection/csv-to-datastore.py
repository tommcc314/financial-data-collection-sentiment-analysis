# This python script takes as input the stock ticker, and file path to a csv with dates, prices and volumes.
# It stores the contents of the csv file in the yahoo-finance-stock-prices datastore entity.
# Parameters: The ticker and csv file path as a string
# Example call of this script: python csv-to-datastore.py "AAPL" "yf-csv/AAPL.csv"

from google.cloud import datastore
import csv
import sys
client = datastore.Client()
kind = 'yahoo-finance-stock-prices'
ticker = sys.argv[1]
with open(sys.argv[2], 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    #loop over the rows
    for row in csv_reader:
        date = row[0]
        price = row[1]
        volume = row[2]
        entity = datastore.Entity(client.key(kind))
        entity.update({
            "Date":date,
            "Stock Price": price,
            "Ticker": ticker,
            'Trading Volume': volume
        })
        client.put(entity)