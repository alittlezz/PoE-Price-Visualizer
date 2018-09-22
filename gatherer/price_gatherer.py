from gatherer import UniqueNamesGatherer as UNG
from gatherer import UniqueCleaner as UC
import pandas as pd
import bs4 as bs
import urllib.parse
import urllib.request
import urllib
import gzip
import io
import time
import math
import os

dataFileName = "Unique Data.csv"
dataFileNameHC = "Unique Data HC.csv"
uniqueFileName = "uniqueNames.txt"
leagueName = "Delve"
leagueNameHC = "Hardcore Delve"
pageUrl = "http://poe.trade/search"

monthToInt = {
	"Jan": 1,
	"Feb": 2,
	"March": 3,
	"April": 4,
	"May": 5,
	"June": 6,
	"July": 7,
	"Aug": 8,
	"Sep": 9,
	"Oct": 10,
	"Nov": 11,
	"Dec": 12
}

monthToString = {
	1: "Jan",
	2: "Feb",
	3: "March",
	4: "April",
	5: "May",
	6: "June",
	7: "July",
	8: "Aug",
	9: "Sep",
	10: "Oct",
	11: "Nov",
	12: "Dec"
}

def saveToFile(items):
	file = open(uniqueFileName, "w")
	for item in items:
		file.write(item + '\n')

def getUniquesFromFile():
	uniques = []
	for unique in open(uniqueFileName, "r", encoding = "latin-1").readlines():
		uniques.append(unique.rstrip())
	return uniques

def createCsv(uniques, csv_name):
	df = pd.DataFrame()
	df["Date"] = pd.Series()
	for unique in uniques:
		df[unique] = pd.Series()
	df.to_csv(csv_name, index = False)

def updateCsv(date, prices, csv_name):
	newRow = prices
	newRow.insert(0, date)
	df = pd.read_csv(csv_name, encoding = "latin1")
	df.loc[-1] = newRow
	df.to_csv(csv_name, index = False)

def extract_price(item, ratios):
	try:
		nr = item["data-buyout"].split()[0]
	except IndexError:
		return -1
	curr = item["data-buyout"].split()[1]
	if curr == "chaos":
		return float(nr)
	if curr in ratios:
		if ratios[curr] == -1:
			return -1
		return float(nr) / ratios[curr]
	return -1

f = open("scams.txt", "w")

def getAveragePrice(itemName, ratios, league):
	data = {
		"name" : itemName,
		"league" : league,
		"online" : "on"
	}
	data = urllib.parse.urlencode(data)
	data = data.encode("utf-8")
	req = urllib.request.Request(pageUrl, data)
	req.add_header("Accept-Encoding", "gzip")
	req = urllib.request.urlopen(req)
	buf = io.BytesIO(req.read())
	file = gzip.GzipFile(fileobj = buf)
	data = file.read()
	soup = bs.BeautifulSoup(data, "lxml")

	table = soup.findAll("table", {"class" : "search-results"})
	if len(table) == 0:
		print("No results for " + itemName)
		return -1
	aux = []
	for tbl in table:
		aux = aux + tbl.findAll("tbody")
	table = aux
	if len(table) == 0:
		print("No results for " + itemName)
		return -1

	results = int(math.ceil(0.15 * len(table)))
	table = table[:results]
	average = 0
	prices = []
	for i in range(0, len(table)):
		prices.append(extract_price(table[i], ratios))
	prices = sorted(list(filter(lambda price : price > 0, prices)))
	start_i = 0
	for i in range(0, min(3, len(prices) - 1)):
		if prices[i] <= 0.8 * prices[i + 1]:
			start_i = i + 1
	prices = prices[start_i:]
	for i, price in enumerate(prices):
		average += price
	try:
		return average / len(prices)
	except ZeroDivisionError:
		return 0

def gatherPrices(league):
	ratios = getCurrencyRatios(league)
	prices = []
	uniques = getUniquesFromFile()
	for i, unique in enumerate(uniques):
		unique = unique.rstrip()
		price = getAveragePrice(unique, ratios, league)
		price = int(price * 100) / 100
		prices.append(price)
		# if i%5 == 0:
		# 	print(i / len(uniques) * 100)
	return prices

def getCurrencyNames():
	req = urllib.request.Request("http://currency.poe.trade/")
	req.add_header("Accept-Encoding", "gzip")
	req = urllib.request.urlopen(req)
	buf = io.BytesIO(req.read())
	file = gzip.GzipFile(fileobj = buf)
	data = file.read()
	soup = bs.BeautifulSoup(data, "lxml")

	table = soup.findAll("div", {"class" : "selector-contents"})[0]
	table = table.findAll("div", {"class" : "has-tip currency-selectable currency-square "})
	file = open("currencyNames.txt", "w")
	for div in table:
		file.write(div["data-title"] + ' ' + div["data-id"] + '\n')

def getCurrencyRatio(id, league):
	req = urllib.request.Request("http://currency.poe.trade/search?league=" + league + "&online=x&want=" + id + "&have=4")
	req.add_header("Accept-Encoding", "gzip")
	req = urllib.request.urlopen(req)
	buf = io.BytesIO(req.read())
	file = gzip.GzipFile(fileobj = buf)
	data = file.read()
	soup = bs.BeautifulSoup(data, "lxml")
	table = soup.findAll("div", {"class" : "displayoffer"})
	if len(table) == 0:
		print("No results for " + id)
		return -1
	results = int(math.ceil(0.15 * len(table)))
	table = table[:results]
	average = 0
	prices = []
	for offer in table:
		prices.append(float(offer["data-sellvalue"]) / float(offer["data-buyvalue"]))
	prices = sorted(list(filter(lambda price : price > 0, prices)), reverse = True)
	start_i = 0
	for i in range(0, min(3, len(prices) - 1)):
		if prices[i] * 0.8 >= prices[i + 1]:
			start_i = i + 1
	prices = prices[start_i:]
	for i, price in enumerate(prices):
		average += price
	try:
		return average / len(prices)
	except ZeroDivisionError:
		return 0

def getCurrencyRatios(league):
	file = open("gatherer/currencyNames.txt", "r")
	ratios = {}
	for currency in file.readlines():
		currency = currency.split()
		id = currency[-1]
		name = ""
		for part in currency[:-1]:
			name = name + part + ' '
		name = name.rstrip()
		ratios[name] = getCurrencyRatio(id, league)
	return ratios

def getDate():
	return time.strftime("%d") + " " + monthToString[int(time.strftime("%m"))]

def main():
	#uniques = UNG.getUniqueNames()
	#uniques = UC.cleanUniques(uniques)
	#saveToFile(uniques)

	#uniques = getUniquesFromFile()
	#createCsv(uniques, dataFileNameHC)
	#createCsv(uniques, dataFileName)
	start = time.time()
	prices = gatherPrices(leagueName)
	updateCsv(getDate(), prices, dataFileName)

	print("Finished loading ", leagueName, " items")

	prices = gatherPrices(leagueNameHC)
	updateCsv(getDate(), prices, dataFileNameHC)

	print("Finished loading ", leagueNameHC, " items")
	#os.system("shutdown -s -t 0")

#main()