#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: add search phrases
# 

import urllib
from bs4 import BeautifulSoup
from collections import Counter
import os
import re

maxAnalysisCount = 150
maxOutputCount = 100
outFileName = "CraftConfWordFreqTrend.csv"
commonWordsFileName = "CommonWords.csv"	

def readList(input, separator=''):
	retList = list()
	with open(input, 'rb') as inputFile:
		for line in inputFile:
			outline = line.strip()
			if outline != "" and not outline.startswith("#"):
				if separator == '':
					retList.append(outline)
				else:
					for item in outline.split(separator):
						item = item.strip()
						if item != "":
							retList.append(item)
    	return retList

def writeHeader(outFileName):
	try:
		os.remove(outFileName)
	except OSError:
		pass
	with open(outFileName, "a") as outfile:
		outfile.write("{0}, {1}, {2}\n".format("Year", "Keyword", "Frequency"))

def parsePage(url, outFileName, prefix):
	print "Processing URL: {0}, Result: {1}, Prefix: {2}".format(url, outFileName, prefix)
	opener = urllib.urlopen(url)
	page = opener.read()
	opener.close()
	soup = BeautifulSoup(page, "html.parser", from_encoding="UTF-8")
	content = soup.find_all("li", "speakers-item")
	text = ""
	for entry in content:
		text += entry.get_text(" ", True)
	words = [word.lower() for word in text.split()]
	c = Counter(words)
	for key in commonWords:
			if key in c:
				del c[key]

	mostCommon = list()
	for word, count in c.most_common(maxAnalysisCount):
		if not re.search('[–{@#!;+=_,$<(^)>?.:%/&}''"''-]', word):
			if not (re.search(u'\u2014', word) or re.search(u'\u2013', word)):
				if not re.search('[0-9]', word):
					if word:
						mostCommon.append((word, count))
					else:
						print("Skipping: <empty>")
				else:
					print("Skipping number: {0}".decode('ascii', 'ignore').format(word))
			else:
				print("Skipping unicode character: {0}".decode('ascii', 'ignore').format(word))
		else:
			print("Skipping special character: {0}".decode('ascii', 'ignore').format(word))

	with open(outFileName, "a") as outfile:
		for word, count in mostCommon[:maxOutputCount]:
			outfile.write("{0}, {1}, {2}\n".format(prefix, word, count))
	print "Done"

# main
commonWords = readList(commonWordsFileName, ',')
writeHeader(outFileName)
parsePage("https://web.archive.org/web/20160325231108/http://craft-conf.com/2016", outFileName, "year2016")
parsePage("https://web.archive.org/web/20160406212403/http://craft-conf.com/2015", outFileName, "year2015")
parsePage("https://web.archive.org/web/20160324192950/http://craft-conf.com/2014", outFileName, "year2014")


