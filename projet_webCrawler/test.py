url = 'https://www.liaoxuefeng.com/wiki/896043488029600'
link = '/wiki/896043488029600/900062620154944/111/222'

urls=[]
links=[]

urls = str(url).split('/')
links = str(link).split('/')

print(urls)
print(links)

link = []

_link = urls+links

list(link.append(l) for l in _link if not l in link)

a = '/'.join(link)

print(link)
print(a)



'''
for i in str(url).split('/'):
    urls.append(i)

for i in str(link).split('/'):
    links.append(i)

print(urls)
print(links)

lastIndex = 0

for k in links:
    if k in urls:
        lastIndex = links.index(k)

print(url+'/'+links[lastIndex+1])
'''