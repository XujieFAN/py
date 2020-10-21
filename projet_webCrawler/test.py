from downloadHTML import DownloadHTML
import requests
from bs4 import BeautifulSoup

url = 'http://www.ityouknow.com/python/2019/07/31/python-plan-100.html'
#url2 = 'https://www.liaoxuefeng.com/wiki/896043488029600/898732792973664'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
            'Content-Type':'text/html',
            'Accept-Language':'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5'}
#path_selector = '#x-sidebar-left-content'

page1 = DownloadHTML(url, headers, 'test/','test1.html')
#page2 = DownloadHTML(url2, headers, 'test/','test2.html')

#page1.downloadHtml()
#page2.downloadHtml()

res = requests.get(url, headers=headers)
print(requests.Response)
'''
html = BeautifulSoup(res.text,'lxml')

#extract links, script
[tag.extract() for tag in html.select('head link')]
[tag.extract() for tag in html.select('head script')]

#for images
SRCs_dict = page1.getImageSRCs_fromHTML(html)
imgLocalNames = page1.getImages_fromSRCs(SRCs_dict.values())
for imgSrc in html.find_all('img'):
    imgSrc['src'] = imgLocalNames[SRCs_dict[imgSrc['src']]]

page1.html2file(str(html),page1.savedHtmlName)
'''