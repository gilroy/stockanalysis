import urllib.error, urllib.parse
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as matTicker
import matplotlib.dates as matDates
import matplotlib.finance
import matplotlib
import pylab
from urllib.request import urlopen

# EMA = (closePrice - EMA(previous day)) x multiplier + EMA(previous day)
def exponentialMovingAverage(data, window):
	weights = np.exp(np.linspace(-1.,0.,window))
	# simple moving average
	weights /= weights.sum()
	# convolve() accounts for  EMA multiplier
	a = np.convolve(data, weights, mode = "full")[:len(data)]
	a[:window] = a[window]
	return a

# date conversion used in graphStockData(). Found on stackOverflow because strpdate2num() threw errors in python 3
def bytesdate2num(fmt, encoding='utf-8'):
    strconverter = matDates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def graphStockData(symbol):
	# assign variables from file and format date (element 0)
	date, closePrice, highPrice, lowPrice, openPrice, volume = np.loadtxt(symbol + ".txt",delimiter=',', unpack=True,converters={ 0: bytesdate2num("%Y%m%d")})

	# store variables in list elements so candlestick() can interpret it
	x = 0
	y = len(date)
	candleArray = []
	while x < y:
		appendData = date[x], openPrice[x], closePrice[x], highPrice[x], lowPrice[x], volume[x]
		candleArray.append(appendData)
		x += 1

	fig = plt.figure()
	ax = plt.subplot(1,1,1)# (1,1,1) defines 1 grid

	# graph in the form of candles
	candlestick(ax, candleArray, width=.75, colorup="g", colordown="r")

	movingAvg1 = 50
	movingAvg2 = 200
	# plot the moving averages
	ax.plot(date, exponentialMovingAverage(closePrice, movingAvg1))
	ax.plot(date, exponentialMovingAverage(closePrice, movingAvg2))


	# clean up the looks (titles, grid, adjusting FOV)
	title = " Historical Stock Data"
	fig.suptitle(symbol + title)
	ax.grid(True, color="b")
	plt.subplots_adjust(left = .10,bottom=.17,right=.94,top=.90,wspace=.20,hspace=.20)
	plt.xlabel('Date', fontsize=18)
	plt.ylabel('Stock Price ($)', fontsize=16)
	for dates in ax.xaxis.get_ticklabels():
            dates.set_rotation(35)

    # format dates- how many and how to display them
	ax.xaxis.set_major_locator(matTicker.MaxNLocator(10))
	ax.xaxis.set_major_formatter(matDates.DateFormatter("%Y-%m-%d"))

	plt.show()


def getStockData(stockToGet):
	# yahoo finance API
	url = "http://chartapi.finance.yahoo.com/instrument/1.0/" + stockToGet + "/chartdata;type=quote;range=2y/csv"
	saveFileName = stockToGet + ".txt"

	saveFile = open(saveFileName, "w")

	source = urlopen(url).read()
	splitSource = str(source, encoding="utf-8").split("\n")
	# parse file and write to a new file
	for line in splitSource:
		if "values" not in line:
			splitLine = line.split(",")
			if len(splitLine) == 6:
				write = line + "\n"
				saveFile.write(write)
	saveFile.close()

	pulled = "Pulled data for "
	print(pulled, stockToGet)

	graphStockData(stockToGet)

def main():
	stock = input("Enter stock symbol: ")
	print("Pulling ", stock)
	getStockData(stock)


main()
