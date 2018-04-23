# -*- encoding: utf-8 -*-
import re
import sys
from bs4 import BeautifulSoup
import numpy as np
import time
import datetime

def table_parse(table):
	"""
	"""
	data = []
	playids = []
	_detail = []
	rows = table.find_all('tr')
	for row in rows:
		cols = row.find_all('td')
		
		try:
			cols_value = []
			res = [ele for ele in cols[6].text.strip("\r").split("\n") if len(ele) != 0]
			a = res[1].split(".")
			a1, a2 = a[0] + "." + a[1][0:-1], a[1][-1] + "." + a[2]
			b = res[3].split(".")
			b1, b2 = b[0] + "." + b[1][0:-1], b[1][-1] + "." + b[2]
		except Exception as e:
			continue

		score = res[2]
		num = re.findall(r'\d+', cols[0].text)
		num = num[0]
		playid = row["playid"]
		playids.append(playid)
		for ele in cols:
				ele = ele.text
				if ele is None: ele = ""
				ele = ele.replace("\n", "")
				ele = ele.replace("\r", "")
				ele = ele.replace(" ", "")
				cols_value.append(ele)
		side = cols_value[3].split("[")[0]
		home = cols_value[5].split("]")[1]
		_detail.append([playid, num, side, home, a1, a2, score, b1, b2])
		print num, side, home, a1, a2, score, b1, b2
		
		data.append([ele for ele in cols_value if ele])
	return data, playids, _detail

def main():
	"""
	"""
	with open(sys.argv[1]) as file_obj:
		html_doc = file_obj.read()
	html_doc = html_doc.replace("</br>", "")
	soup = BeautifulSoup(html_doc, 'html.parser')

	data = soup.find('table', {"class": "mb"})
	table, playids, detail = table_parse(data)
	date = datetime.datetime.now().strftime("%Y%m%d") 
	file_write = open("../list/%s" % sys.argv[2], 'wb+')
	for key in playids:
			value = "http://fenxi.zgzcw.com/lq/%s/bfyc" % key
			file_write.write(value + "\n")
	file_write.close()
	
	file_write = open("../detail/%s" % sys.argv[2], "wb+")
	for key in detail:
			file_write.write(",".join(key) + "\n")
	file_write.close()

	for ele in table:
		print "\t".join(ele)

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")
	main()
