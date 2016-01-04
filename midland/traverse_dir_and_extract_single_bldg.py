from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1
import urllib.request,urllib.parse
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import sys
import time
from random import randint
import json

def getQueryListFromLink(href):
	o = urlparse(href)
	return o.query.split("&")

def getQueryDictFromLink(href):
	rows = getQueryListFromLink(href)
	results = {}
	for row in rows:
		arr = row.split("=")
		results[arr[0]]=arr[1]
	return results
def getBs(url):
	try:
		headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
		d = {}
		data = urllib.parse.urlencode(d).encode("utf-8")
		req = urllib.request.Request(url, data, headers)
		# print(type(req))
		html = urllib.request.urlopen(req)
		# print(type(html))
		# html = urlopen(url)
	except HTTPError as e:
		return None
	try:
		bsObj = BeautifulSoup(html.read().decode('big5', 'ignore'),"html.parser")
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
	# print(bldg_link_list)
	# print(len(bldg_link_list))
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


def getDetachedHouseInfo(soupObj):
	try:
		bldg_info = {}

		bldg_name = soupObj.find("font",{"id":"title_name"}).get_text()
		test = soupObj.find("table",{"style":"width:100%;padding:0px;"})
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
def getEstInfo(soupObj):
	try:
		extract=(soupObj.find("img",{"src":"http://resources.midland.com.hk/images/ebook/zh_HK/title_pinfo_revamp.jpg"}).parent.parent.parent).next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
		# extract = soupObj.find("table",{"style":"background-image: url('http://esfphoto.midland.com.hk/img_wm.php?wm=mr&src=&hwm=Y&w=250&h=150&crop=n'); background-repeat: no-repeat; background-position: 500px 20px;"})
		extract1 = extract.findAll("tr",{"valign":"TOP"})
		estate_info = {}
		for row in extract1:
			extract2 = row.find("td",{"class":"title"})
			extract3 = row.find("td",{"class":"content"})
			estate_info_key = extract2.get_text().strip('：')
			# estate_info_value = extract3.get_text().strip('\r\n\t')
			estate_info_value = re.sub(r"\s+","",extract3.get_text())
			estate_info[estate_info_key] = estate_info_value
	except AttributeError as e:
	#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError	
		return None
	return estate_info



def getEstIdFromFile(afile):
	try:
		your_list = []
		f = open(afile,'rt') 
		mystr = f.read()
		my_list = mystr.split(",")
		# reader = csv.reader(f)
		# for row in reader:
		# 	your_list.append(row)
	finally:
		f.close()
	print(my_list)
	return my_list


# main starts
try:
	error_log = open(sys.argv[3],'wt')
	f = open(sys.argv[1],'wt')
	writer = csv.writer(f,delimiter=',')
	writer_error_log = csv.writer(error_log)
	# writer.writerow([result])

	# title = getTitle("http://proptx.midland.com.hk/utx/index.jsp?est_id=E00108&lang=zh")
	# red hill
	# soup = getBs("http://proptx.midland.com.hk/utx/index.jsp?est_id=E00106&lang=zh")
	# est_id_list=['E00110']
	# est_id_list=['E00110', 'E07457', 'E00765', 'E00112','E00106','E11432']
	est_id_list=getEstIdFromFile(sys.argv[2])

	est_links = [ "http://proptx.midland.com.hk/utx/index.jsp?lang=zh&est_id=" + est_id for est_id in est_id_list]
	est_info_links = [ "http://app.midland.com.hk/residential_ebook/default.jsp?lang=zh&estId=" + est_id for est_id in est_id_list]
	for index in range(len(est_id_list)):
		moresoup = getBs(est_info_links[index])
		est_info_extract_dict = getEstInfo(moresoup)
		soup = getBs(est_links[index])
		link_list = getBldgLinks(soup)
		for row in range(len(link_list)):
			
			# pretend to be human
			time.sleep(randint(10,100)/1000+randint(2,5))
			print('Before: %s' % time.ctime())
			input_link = link_list[row]

			is_not_detached_house = re.match("^(http)",input_link)
			# skip the detached house for now
			if is_not_detached_house:

				soup1 = getBs(input_link)
				test = getBldgInfo(soup1)
				if est_info_extract_dict:
					test.update(est_info_extract_dict)
				# print(est_info_extract_dict)
				# print(test)
				writer.writerow([test])
				# writer.writerow([test,est_info_extract_dict])
				# test = getDetachedHouseInfo(soup1)
				# writer.writerow(json.dumps(test))
				# print("\n")
				print(test)
			else:
				writer_error_log.writerow([input_link])
				print("notOK:" )
				# writer_error_log.writerow([getQueryDictFromLink(input_link)])
				print(getQueryDictFromLink(input_link))
		time.sleep(randint(10,100)/1000+randint(3,7))
finally:
	f.close()
