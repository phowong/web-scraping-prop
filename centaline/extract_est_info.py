from bs4 import BeautifulSoup
import re
import sys
import urllib.request,urllib.parse
from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1
from pprint import pprint
from urllib.error import HTTPError
import json

def getBs(url):
	try:
		headers = {
		    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		    'upgrade-insecure-requests': "1",
		    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
		    'referer': "http//www1.centadata.com/ephome.aspx",
		    'accept-language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
		    'cookie': "ASP.NET_SessionId=0xi3ng45zwmdm3553df5wsqi; centadatawatch0=; centadatawatch1=; centadatawatch2=; centadatawatch3=; centadatawatch4=2SSPPWPPYPS; centadatawatch5=1SSPWBPDYPE; Hm_lvt_ead590637b73af1b8bfba9fed484517e=1453256723,1453261712,1453261855,1453263361; Hm_lpvt_ead590637b73af1b8bfba9fed484517e=1453264229; _ga=GA1.2.1204140034.1453256481; __utmt=1; __utma=127968138.1204140034.1453256481.1453261713.1453274643.3; __utmb=127968138.9.10.1453274643; __utmc=127968138; __utmz=127968138.1453261713.2.2.utmcsr=estate.centadata.com|utmccn=(referral)|utmcmd=referral|utmcct=/pih09/pih09/estate.aspx",
		    'cache-control': "no-cache",
		    # 'Content-Type': "text/html;charset=BIG5"
		    }
		d = {}
		data = urllib.parse.urlencode(d).encode("utf-8")
		req = urllib.request.Request(url, data, headers)
		# req = urllib.request.Request(url)
		html = urllib.request.urlopen(req)
	except HTTPError as e:
		print(req.raise_for_status())
		return None
	try:
		bsObj = BeautifulSoup(html.read().decode('utf-8', 'replace'),"html.parser")
	except AttributeError as e:
		#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError
		return None
	return bsObj

def getEstInfo(soupObj):
	try:
		result = {}
		full_path_to_bldg = soupObj.find("a",{"class":"aMenuName","href":"http://hk.centadata.com/pih09/pih09/pasttranindex.aspx"}).parent.get_text()
		full_path_to_bldg_str = re.sub(r"\s+","",full_path_to_bldg)
		print(full_path_to_bldg_str[7:])
		result["breadcrumb"] = full_path_to_bldg_str[7:]
		ct_bldg_name = soupObj.find("b",{"style":"font-size: 15px;"}).get_text()
		result['ct_bldg_name'] = re.sub(r"\s+","",ct_bldg_name)
		extract1 = soupObj.find("td",{"class":"tdSmrTopic"}).parent.parent
		extract2 = extract1.findAll("tr")
		for tr in extract2:
			title = re.sub(r"[\s:]+","",tr.find("td",{"class":"tdSmrTopic"}).get_text())
			content = re.sub(r"\s+","",tr.find("td",{"class":"tdSmrContent"}).get_text())
			result[title]=content

		floor_nos = []
		floor_nos_node = soupObj.find("td",{"style":"height: 57px; vertical-align: middle; font-weight: bold;"})
		extract3 = floor_nos_node.parent.parent.findAll("b")
		for b in extract3:
			txt = re.sub(r"\s+","",b.get_text())
			floor_nos.append(txt)
		result['floor_nos'] = ','.join(floor_nos)

	except AttributeError as e:
	#if the server did not exist, html would be a None object, and html.read() would throw an AttributeError	
		return None
	return result

def getEstLinks(soupObj):
	# for link in soupObj.select( '#unitTran-left .unitTran-left-a td a'):
	# 	print(link['href'])
	return [ link['href'] for link in soupObj.select( '#unitTran-left .unitTran-left-a td a')]
# main start
# getBs("http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=101&page=0")
print(sys.stdin.encoding, sys.stdout.encoding)
print(sys.getdefaultencoding())
# link = "http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=2&code=SDDSGPWASK&ci=zh-hk"
link = "http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=3&code=XSHNIHSXHT&ci=zh-hk"
# link = "http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type={0}&code={1}&ci=zh-hk".format("2","SSPPWPPYPS")
# bldgInfo = getEstInfo(getBs(link))

# pprint(bldgInfo)
# print(json.dumps(bldgInfo, sort_keys=True,indent=4, separators=(',', ': ')))




# with open(sys.argv[1],'wt') as f:
# 	f.write('\n'.join(singlePagePara)) 
# f.close()
