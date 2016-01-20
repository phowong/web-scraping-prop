from bs4 import BeautifulSoup
import re
import sys
from pprint import pprint


def getExtract(soupObj):
	try:
		extract1 = soupObj.find("img",{"src":"img\escopelist.gif"}).parent.parent.parent
		extract2 = extract1.findAll("a")
		extract3 = [ "http://www1.centadata.com/"+ x['href'] for x in extract2]
		# pprint(extract3)
	except AttributeError as e:
	#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError	
		return None
	return extract3

# main start
# link: http://www1.centadata.com/ephome.aspx
file1 = open("/Users/pho/git_2015/web-scraping-prop/centaline/Centadata-dir.html","r", encoding="big5")
bsObj = BeautifulSoup(file1,"html.parser")
f = open(sys.argv[1],'wt')

# convert list to str
f.write(",".join(map(lambda x:str(x), getExtract(bsObj))))
f.close()
