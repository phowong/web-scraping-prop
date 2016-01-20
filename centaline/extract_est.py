from bs4 import BeautifulSoup
import re
import sys
import urllib.request,urllib.parse
from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1
from pprint import pprint
from urllib.error import HTTPError

def getBs(url):
	try:
		headers = {
		    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		    'upgrade-insecure-requests': "1",
		    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
		    'referer': "http//www1.centadata.com/ephome.aspx",
		    'accept-language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
		    'cookie': "ASP.NET_SessionId=0xi3ng45zwmdm3553df5wsqi; centadatawatch0=; centadatawatch1=; centadatawatch2=; centadatawatch3=; centadatawatch4=2SSPPWPPYPS; centadatawatch5=1SSPWBPDYPE; Hm_lvt_ead590637b73af1b8bfba9fed484517e=1453256723,1453261712,1453261855,1453263361; Hm_lpvt_ead590637b73af1b8bfba9fed484517e=1453264229; _ga=GA1.2.1204140034.1453256481; __utmt=1; __utma=127968138.1204140034.1453256481.1453261713.1453274643.3; __utmb=127968138.9.10.1453274643; __utmc=127968138; __utmz=127968138.1453261713.2.2.utmcsr=estate.centadata.com|utmccn=(referral)|utmcmd=referral|utmcct=/pih09/pih09/estate.aspx",
		    'cache-control': "no-cache"
		    }
		d = {}
		data = urllib.parse.urlencode(d).encode("utf-8")
		req = urllib.request.Request(url, data, headers)
		# req = urllib.request.Request(url)
		html = urllib.request.urlopen(req)
	except HTTPError as e:
		return None
	try:
		bsObj = BeautifulSoup(html.read().decode('big5', 'replace'),"html.parser")
	except AttributeError as e:
		#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError
		return None
	return bsObj

def getEstLinkPara(soupObj):
	try:
		result = []
		extract1 = soupObj.findAll("tr",{"onmouseover":"changeColor(this);changeselecticon('1');"})
		extract2 = [ x['onclick'] for x in extract1]
		for x in extract2:
			matchObj = re.search(r'\((.+?)\)', x)
			result.append(matchObj.groups()[0])
	except AttributeError as e:
	#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError	
		return None
	return result

# main start
# getBs("http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=101&page=0")
singlePagePara = getEstLinkPara(getBs("http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=101&page=0"))
print(singlePagePara)
with open(sys.argv[1],'wt') as f:
	f.write('\n'.join(singlePagePara)) 
f.close()
