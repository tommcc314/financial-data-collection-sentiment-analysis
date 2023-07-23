#This code produces a scatterplot of the sentiment score from the 10k versus the stock percent change in value.
import yfinance as yf
import sys
from datetime import datetime, timedelta
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from regression_analysis import LinearModel
# taking input as the date
def stock_history_correlation(
    file_name, 
    ticker, 
    forward, 
    corpus_type,
    xlabel = "S_wa", 
    ylabel = "R_st",
    model = "vX", 
    swa_type = "Compound"
    ):
    def bad_date(Date):
        if forward == "3d" and Begindate + timedelta(days = 3) > datetime.now():
            return True
        if forward == "5d" and Begindate + timedelta(days = 5) > datetime.now():
            return True
        if forward == "2yr" and Begindate + timedelta(days = int(2*365)) > datetime.now():
            return True
        elif forward == "18mo" and Begindate + timedelta(days = int(3*365/2)) > datetime.now():
            return True
        elif forward == "1yr" and Begindate + timedelta(days = int(365)) > datetime.now():
            return True
        elif forward == "6mo" and Begindate + timedelta(days = int(365/2)) > datetime.now():
            return True
        elif forward == "3mo" and Begindate + timedelta(days = int(365/4)) > datetime.now():
            return True
        return False
    history = yf.download(ticker, interval="1d")
    #print(history[9900:9910])
    history["date"] = history.index
    future_from_date = []
    x = []
    #current, 6mo,12mo,18mo,24mo
    with open(file_name) as readfile:
        csv_reader = csv.DictReader(readfile,delimiter= ",")
        for row in csv_reader:
            date_header = "Date of 10k Filing"
            if corpus_type == "Earnings Call":
                date_header = "Date of Earnings Call"
            Begindate = datetime.strptime(row[date_header][0:10], "%Y-%m-%d")
            if(bad_date(Begindate)):
                continue
            future_from_date.append( {
                    "Date":Begindate,
                    "Date Stock":adj_close(Begindate, history),
                    "Date + 3d Stock":adj_close(Begindate + timedelta(days = 3), history), 
                    "Date + 5d Stock":adj_close(Begindate + timedelta(days = 5), history),
                    "Date + 3mo Stock": adj_close(Begindate + timedelta(days = int(365/4)), history),
                    "Date + 6mo Stock": adj_close(Begindate + timedelta(days= int(365/2)), history),
                    "Date + 1yr Stock": adj_close(Begindate + timedelta(days= int(365)), history),
                    "Date + 18mo Stock": adj_close(Begindate + timedelta(days= int(3*365/2)), history),
                    "Date + 2yr Stock": adj_close(Begindate + timedelta(days= int(2*365)), history),
            })
            x.append(float(row[swa_type]))

    x = np.array(x)
    y = []
    for date in future_from_date:
        y.append( (date[f"Date + {forward} Stock"] -  date["Date Stock"]) / date["Date Stock"]  )
        print(f'{y[-1]*100}% is the return if you invested for {forward} starting on {date["Date"]}' )
    y = np.array(y)
    print(x)
    print(y)
    with open("zsample.txt", mode = 'w') as f:
        f.write( f'{swa_type} Sentiment Score on {ticker}_{corpus_type} vs {forward} Return data points\n')
        f.write("Date\tS_wa\tR_st\n")
        for i in range(len(y)):
            f.write(f'{str(future_from_date[i]["Date"])[0:10]}\t{x[i]}\t{y[i]}\n')
    plt.plot(x,y,'o')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    info = LinearModel(x,y)
    print(info)
    line_input = np.linspace(min(x), max(x))
    plt.plot(line_input, info["Coef"][0]*line_input + info["Intercept"], label = info["Text"], c = 'red' )
    plt.legend(loc='best')
    plt.title(f' {swa_type} Sentiment Score on {ticker}_{corpus_type} vs {forward} Return')
    plt.savefig(f"{ticker}_{corpus_type}_{forward} {swa_type} Sentiment {model}.png")

def adj_close(date, history):
    lo = 0
    hi = len(history)-1
    while(hi != lo):
        mid = int((lo + hi)/2)
        midDate = datetime.strptime(str(history.iloc[mid]["date"])[0:10], "%Y-%m-%d") 
        if midDate > date:
            hi = mid
        else:
            lo = mid+1
    #print(f'{date} vs {datetime.strptime(str(history.iloc[lo]["date"])[0:10], "%Y-%m-%d")}')
    return history.iloc[lo]["Adj Close"] 
if __name__ == "__main__":
    stock_history_correlation(file_name = sys.argv[1], ticker = sys.argv[2], forward = "5d", corpus_type = "10K", model = "v2")
