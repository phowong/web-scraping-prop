from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import sys
import time
from random import randint
def getBs(url):
	try:
		html = urlopen(url)
	except HTTPError as e:
		return None
	try:
		bsObj = BeautifulSoup(html.read(),"html.parser")
	except AttributeError as e:
		#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError
		return None
	return bsObj

def getBldgLinks(soupObj):
	try:
		bldg_link_list = []
		bldg_Curr = soupObj.find("tr",{"class":"bldg_Curr"})
		bldg_NotCurr = soupObj.findAll("tr",{"class":"bldg_NotCurr"})
		
		bldg_Curr_link = bldg_Curr.find("td").find("a")["href"]
		bldg_link_list.append(bldg_Curr_link)
		
		for row in bldg_NotCurr:
			bldg_NotCurr_link = row.find("td").find("a")["href"]
			bldg_link_list.append(bldg_NotCurr_link)

	except AttributeError as e:
	#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError	
		return None
	print(bldg_link_list)
	print(len(bldg_link_list))
	return bldg_link_list

def getBldgInfo(soupObj):
	try:
		bldg_info = {}

		bldg_name = soupObj.find("font",{"id":"title_name"}).get_text()
		test = soupObj.find("table",{"style":"width:100%;padding-top:3px;"})
		test2 = test.findAll("td",{"class":"tdBottom"})
		extract1 = []
		for row in test2:
			extract1.append(re.sub(r"\s+","",row.get_text()))
		
		extract2 = [v.split(":",1) for v in extract1]
		bldg_info["bldg_name"]=re.sub(r"\s+","",bldg_name)
		for row in extract2:
			bldg_info[row[0]]=row[1]

	except AttributeError as e:
	#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError	
		return None
	return bldg_info


# title = getTitle("http://proptx.midland.com.hk/utx/index.jsp?est_id=E00108&lang=zh")
# red hill
soup = getBs("http://proptx.midland.com.hk/utx/index.jsp?est_id=E00106&lang=zh")

# mk
# soup = getBs("http://proptx.midland.com.hk/utx/index.jsp?est_id=E000015311&lang=zh")

link_list = getBldgLinks(soup)
print(link_list)

for row in range(0,9):
# for row in range(len(link_list)):
	
	print(row)
	print(link_list[row])
	time.sleep(randint(10,100)/1000+randint(2,5))
	print('Before: %s' % time.ctime())
	soup1 = getBs(link_list[row])
	test = getBldgInfo(soup1)
	print(test)


if test == None:
	print("error write to file")
else:
	print("good la")
	try:
		f = open(sys.argv[1],'wt')
		# writer = csv.writer(f, delimiter=",",quoting=csv.QUOTE_ALL)
		writer = csv.writer(f)
		# writer.writerow([result])
		for row in test:
			writer.writerow([row])
	finally:
		f.close()

