import requests
from bs4 import BeautifulSoup
import lxml
import time
import os

class DownloadHTML(object):
    def __init__(self, url, headers, path, name, path_selector=None):
        self.url = url
        self.headers = headers
        self.path_selector = path_selector
        self.savePath = path
        self.savedHtmlName = name
        self.encoding = 'utf8'

    def setRequestEncoding(self, encoding):
        self.encoding = encoding

    def getSelectedHTML(self):
        try:
            res = requests.get(self.url, headers=self.headers)
            html = res.text.encode(self.encoding)

        except ConnectionError:
            print('problem connexion')

        else:
            soup = BeautifulSoup(html,'lxml')
            if self.path_selector != None:
                tagFormat_selectedHTML = soup.select_one(self.path_selector)
                return tagFormat_selectedHTML
            else:
                return soup

    #if html is soup, call html2file(str(html),...)
    def html2file(self, html, file, mode='a+', encoding='utf-8'):
        file = self.savePath + file
        
        try:
            with open(file,mode,encoding=encoding) as f:
                f.write(html)
            return True
        except:
            return False

    def getHrefs_fromHTML(self, html, tryGetCompletHrefs=0):
        resultSet = html.find_all('a')

        links = list()

        for result in resultSet:
            if result.get('href')[0:1] != '#':
                links.append(result.get('href'))
        
        if tryGetCompletHrefs == 1:
            hrefs = list()
            for link in links:
                hrefs.append(try_add_OneLink_to_url(link, self.url))
            return hrefs
        else:
            return links

    def try_add_OneLink_to_url(self, link):
        segments_url = str(self.url).split('/')
        segments_link = str(link).split('/')
        link = list()

        _link = segments_url + segments_link

        list(link.append(l) for l in _link if not l in link)

        list_complet = '/'.join(link)
        
        return list_complet

    def getImageSRCs_fromHTML(self, html):
        # url should be like https://www.liaoxuefeng.com/xxx
        host = 'https://' + self.url.split('/')[2]
        resultSet = html.find_all('img')

        SRCs_dict = dict()

        for result in resultSet:
            if result.get('src')[0:4] == 'http':
                SRCs_dict[result.get('src')] = result.get('src')
            else:
                SRCs_dict[result.get('src')] = host + result.get('src')
        
        return SRCs_dict

    def getContentType_fromHeaders(self, headers):
        if headers['content-type'].split('/')[0] == 'image':
            if '+' not in headers['content-type'].split('/')[1]:
                content_type = headers['content-type'].split('/')[1]
            elif 'svg' in headers['content-type'].split('/')[1]:
                content_type = 'svg'
            else:
                content_type = None

        return content_type

    #if SRCs is dict, call getImages_fromSRCs(SRCs.values())
    def getImages_fromSRCs(self, SRCs):
        savePath_img = self.savePath + 'img'
        if not os.path.exists(savePath_img):
            os.makedirs(savePath_img)
        
        imgLocalNames = dict()
        i = 0
        for src in SRCs:
            i = i+1
            try:
                img = requests.get(src, headers=self.headers)
                img_type = self.getContentType_fromHeaders(img.headers)
                img_name = str(int(time.time()))+'_'+str(i)+'.'+img_type
            except ConnectionError:
                print('problem connexion for src={}'.format(src))
            else:
                self.html2file(img.content,'img/'+img_name, mode='wb+', encoding=None)
                imgLocalNames[src] = 'img/'+img_name

        return imgLocalNames

    def downloadHtml(self, selectorToExtract=['head link','head script']):
        if self.path_selector != None:
            html = self.getSelectedHTML()
        else:
            html = self.getSelectedHTML()

        #extract links, script
        for selector in selectorToExtract:
            [tag.extract() for tag in html.select(selector)]
        
        #for images
        SRCs_dict = self.getImageSRCs_fromHTML(html)
        imgLocalNames = self.getImages_fromSRCs(SRCs_dict.values())
        for imgSrc in html.find_all('img'):
            imgSrc['src'] = imgLocalNames[SRCs_dict[imgSrc['src']]]

        self.html2file(str(html),self.savedHtmlName)


if __name__ == "__main__":
    url = 'https://www.liaoxuefeng.com/wiki/896043488029600'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
    
    # path_selector optional
    page = DownloadHTML(url, headers, 'test/', 'test.html')
    
    #page.setRequestEncoding('ISO-8859-1') #for Chinese

    # selectorToExtract optional
    page.downloadHtml()
