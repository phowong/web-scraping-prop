from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
def getEstBdgLinks(url):
	try:
		html = urlopen(url)
	except HTTPError as e:
		return None
	try:
		bsObj = BeautifulSoup(html.read(),"html.parser")
		title = bsObj.findAll({"class":"bg_content_search"})
	except AttributeError as e:
		#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError
		return None
	return title

def getBuildingName(url):
	try:
		html = urlopen(url)
	except HTTPError as e:
		return None
	try:
		bsObj = BeautifulSoup(html.read(),"html.parser")
		title = bsObj.findAll(attrs={"id":"title_name"}).prettify()
	except AttributeError as e:
		#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError
		return None
	return title
def print_batch(dataobj):
	if (dataobj != None) and (len(dataobj)>=1):
		for child in dataobj:
			print(child)

title = getBuildingName("http://proptx.midland.com.hk/utx/index.jsp?bldg_id=B000004182&lang=zh&hidAll=&hidLHS=")
# bdgLinks = getEstBdgLinks("http://proptx.midland.com.hk/utx/index.jsp?est_id=E00108&lang=zh")
if title == None:
	print("building could not be found")
else:
	# print_batch(bdgLinks)
	print(title)