import requests
from bs4 import BeautifulSoup
import lxml
import time


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
            return str(tagFormat_selectedHTML)
        else:
            return str(soup)


def html2file(html, file, mode='a+'):
    file = 'test/'+file
    try:
        with open(file,mode,encoding='utf-8') as f:
            f.write(html)
        return True
    except:
        return False


def getLinks_fromHTML(html, tryGetCompletHrefs=0, url=None):
    soup = BeautifulSoup(html,'lxml')
    resultSet = soup.find_all('a')

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


if __name__ == "__main__":

    html = getSelectedHTML(selectedURL,1,path_selector)

    links = getLinks_fromHTML(html,1,selectedURL)

    #print(links)

    '''
    for page in links:
        filename = str(time.time()).replace('.','-')+'.html'
        html2file(getSelectedHTML(page),filename)
    '''

    filename = str(time.time()).replace('.','-')+'.html'
    html2file(getSelectedHTML(links[1]),filename)

    filename = str(time.time()).replace('.','-')+'.html'
    html2file(getSelectedHTML(links[2]),filename)
