import requests
from bs4 import BeautifulSoup
import lxml
import time
import os


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}

selectedURL = 'https://www.liaoxuefeng.com/wiki/896043488029600'

#F12 --> Copy --> Copy selector
path_selector = '#x-sidebar-left-content'


def getSelectedHTML(selectedURL, withSelector=0, path_selector=None):
    try:
        html = requests.get(selectedURL, headers=headers)

    except ConnectionError:
        print('problem connexion')

    else:
        soup = BeautifulSoup(html.text,'lxml')
        if withSelector == 1 and path_selector != None:
            tagFormat_selectedHTML = soup.select_one(path_selector)
            return tagFormat_selectedHTML
        else:
            return soup

#call html2file(str(html),...)
def html2file(html, file, mode='a+', encoding='utf-8'):
    file = 'test/'+file
    try:
        with open(file,mode,encoding=encoding) as f:
            f.write(html)
        return True
    except:
        return False


def getHrefs_fromHTML(html, tryGetCompletHrefs=0, url=None):
    #soup = BeautifulSoup(html,'lxml')
    #resultSet = soup.find_all('a')
    resultSet = html.find_all('a')

    links = list()

    for result in resultSet:
        if result.get('href')[0:1] != '#':
           links.append(result.get('href'))
    
    if tryGetCompletHrefs == 1 and url != None:
        hrefs = list()
        for link in links:
            hrefs.append(try_add_OneLink_to_url(link, url))
        return hrefs
    else:
        return links


def try_add_OneLink_to_url(link, url):
    segments_url = str(url).split('/')
    segments_link = str(link).split('/')
    link = list()

    _link = segments_url + segments_link

    list(link.append(l) for l in _link if not l in link)

    list_complet = '/'.join(link)
    
    return list_complet


def getImageSRCs_fromHTML(html, url):
    # url should be like https://www.liaoxuefeng.com/xxx
    host = 'https://' + url.split('/')[2]


    #soup = BeautifulSoup(html,'lxml')
    #resultSet = soup.find_all('img')
    resultSet = html.find_all('img')

    #SRCs = list()
    #SRCs_origin = list()

    SRCs_dict = dict()

    for result in resultSet:
        #SRCs_origin.append(result['src'])
        if result.get('src')[0:4] == 'http':
            SRCs_dict[result.get('src')] = result.get('src')
            #SRCs.append(result.get('src'))
        else:
            SRCs_dict[result.get('src')] = host + result.get('src')
            #SRCs.append(host + result.get('src'))
    
    return SRCs_dict
    #SRCs, SRCs_origin


def getContentType_fromHeaders(headers):
    if headers['content-type'].split('/')[0] == 'image':
        if '+' not in headers['content-type'].split('/')[1]:
            content_type = headers['content-type'].split('/')[1]
        elif 'svg' in headers['content-type'].split('/')[1]:
            content_type = 'svg'
        else:
            content_type = None

    return content_type

#if SRCs is dict, call getImages_fromSRCs(SRCs.values())
def getImages_fromSRCs(SRCs):
    if not os.path.exists('test/img'):
        os.mkdir('test/img')
    
    imgLocalNames = dict()
    i = 0
    for src in SRCs:
        i = i+1
        try:
            img = requests.get(src, headers=headers)
            img_type = getContentType_fromHeaders(img.headers)
            img_name = str(int(time.time()))+'_'+str(i)+'.'+img_type
        except ConnectionError:
            print('problem connexion for src={}'.format(src))
        else:
            html2file(img.content,'img/'+img_name, mode='wb+', encoding=None)
            imgLocalNames[src] = 'img/'+img_name

    # to change the src with this img name in html
    return imgLocalNames
    


def test_Get_Html_and_ChgSrcOfImages():
    html = getSelectedHTML(selectedURL)
    SRCs_dict = getImageSRCs_fromHTML(html,selectedURL)
    imgLocalNames = getImages_fromSRCs(SRCs_dict.values())

    [tag.extract() for tag in html.select('head link')]
    [tag.extract() for tag in html.select('head script')]

    for imgSrc in html.find_all('img'):
        print(imgLocalNames[SRCs_dict[imgSrc['src']]])
        imgSrc['src'] = imgLocalNames[SRCs_dict[imgSrc['src']]]

    html2file(str(html),'test.html')


if __name__ == "__main__":

    test_Get_Html_and_ChgSrcOfImages()
