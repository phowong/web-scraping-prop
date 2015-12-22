from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import csv
import sys
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

def getExtract(soupObj):
	try:
		# extract=(soupObj.find("img",{"src":"http://resources.midland.com.hk/images/ebook/zh_HK/title_pinfo_revamp.jpg"}).parent.parent.parent).next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
		extract = soupObj.find("table",{"style":"background-image: url('http://esfphoto.midland.com.hk/img_wm.php?wm=mr&src=&hwm=Y&w=250&h=150&crop=n'); background-repeat: no-repeat; background-position: 500px 20px;"})
		extract1 = extract.findAll("tr",{"valign":"TOP"})
		
		# extract3 = extract1.findAll("td",{"class":"content"})
		output = ""
		for row in extract1:
			# temp_text = row.get_text()
			extract2 = row.find("td",{"class":"title"})
			extract3 = row.find("td",{"class":"content"})
			# for row1 in extract3:
			# 	temp_text = row1.get_text()
			# 	print(temp_text)

			# output += extract2.get_text().lstrip().rstrip() + " " + extract3.get_text().lstrip().rstrip()
			output += extract2.get_text().strip('：') + " " + extract3.get_text().strip()
			output += ",\n"
			# for index in range(len(extract2)):
				# temp_text = extract2[index].get_text()
				# print(index)

	except AttributeError as e:
	#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError	
		return None
	# return extract1
	print(type(output))
	print(output)
	return output

# title = getTitle("http://proptx.midland.com.hk/utx/index.jsp?est_id=E00108&lang=zh")
soup = getBs("http://app.midland.com.hk/residential_ebook/default.jsp?estId=E00105&lang=zh")
result = getExtract(soup)
if result == None:
	print("Title could not be found")
else:
	try:
		f = open(sys.argv[1],'wt')
		# writer = csv.writer(f, delimiter=",",quoting=csv.QUOTE_ALL)
		writer = csv.writer(f)
		writer.writerow(('title1','title2','title3'))
		for i in range(10):
			writer.writerow([result])
	finally:
		f.close()

