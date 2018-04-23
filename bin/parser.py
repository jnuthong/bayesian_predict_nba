# -*- encoding: utf-8 -*-
import re
import sys
from bs4 import BeautifulSoup
import numpy as np
import time

def table_parse(table):
	"""
	"""
	data = []
	rows = table.find_all('tr')
	for row in rows:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		data.append([ele for ele in cols if ele])
	return data

def main():
	"""
	"""
	with open(sys.argv[1]) as file_obj:
		html_doc = file_obj.read()
	soup = BeautifulSoup(html_doc, 'html.parser')

	date = sys.argv[2]

	host_name = soup.find('div', {"class": "visit-name"})
	visit_name = soup.find("div", {"class": "host-name"})
	# print visit_name.text, host_name.text
	hostRecord = soup.find('div', {'class': "hostRecord"})
	vistorRecord = soup.find("div", {"class": "visitorRecord"})

	hostTable = hostRecord.find('table', {"class": "fight-tab"})
	hostData = table_parse(hostTable)
	total_data = []
	side_data = []
	home_data = []
	for ele in hostData:
		if len(ele) == 0: continue
		total_data.append(float(ele[9]))
		if ele[4] != host_name.text: continue
		score = ele[3].split(" ")
		score = score[0].split(":")[1]
		home_data.append(float(score))
		# print "\t".join(ele)

	vistorTable = vistorRecord.find('table', {"class": "fight-tab"})
	vistorData = table_parse(vistorTable)
	for ele in vistorData:
		if len(ele) == 0: continue
		if ele[2] != visit_name.text: continue
		# total_data.append(float(ele[9]))
		score = ele[3].split(":")[0]
		side_data.append(float(score))
		# print "\t".join(ele)
	
	# file_name = visit_name.text + "vs" + host_name.text 
	file_name = str(int(time.time()))
	file_name = "../middle/" + date + "." + file_name
	file_write = open(file_name, "wb+")
	print file_name

	total_index = total_data.index(max(total_data))
	del total_data[total_index]
	total_index = total_data.index(min(total_data))
	del total_data[total_index]

	total_mu = np.mean(total_data)
	total_sigma = np.std(total_data)

	side_index = side_data.index(max(side_data))
	del side_data[side_index]
	side_index = side_data.index(min(side_data))
	del side_data[side_index]


	home_index = home_data.index(max(home_data))
	del home_data[home_index]
	home_index = home_data.index(min(home_data))
	del home_data[home_index]

	side_mu = np.mean(side_data)
	side_sigma = np.std(side_data)
	
	home_mu = np.mean(home_data)
	home_sigma = np.std(home_data)

	file_write.write(" ".join([visit_name.text, host_name.text, str(total_mu), str(total_sigma), str(side_mu), str(side_sigma)]) + "\n")
	file_write.write(",".join(map(str, total_data)) + "\n")
	file_write.write(",".join(map(str, side_data)) + "\n")
	file_write.write(",".join(map(str, home_data)) + "\n")
	file_write.write(" ".join(map(str, [home_mu, home_sigma])) + "\n")
	file_write.close()


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")
	main()
