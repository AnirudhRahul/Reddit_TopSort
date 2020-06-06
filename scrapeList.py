#Scrape http://redditlist.com for all subreddits with over 1000 users
from lxml import html
import requests

def main(cutOff=10000):
    names = []
    sfw = []
    sizes = []
    progress=0
    for i in range(1,50):
        page = requests.get('http://redditlist.com/all?page='+str(i))
        yield progress
        progress+=2
        tree = html.fromstring(page.content)
        topSubs = tree.xpath('//div[@class="span4 listing"]')[1]
        items = topSubs.xpath('.//div[@class="listing-item"]')
        names.extend(topSubs.xpath('.//div[@class="listing-item"]//a/text()'))
        sfw.extend(topSubs.xpath('.//div[@class="listing-item"]/@data-target-filter'))
        temp = topSubs.xpath('.//div[@class="listing-item"]//span[@class="listing-stat"]/text()')
        sizes.extend(int(str.replace(',','')) for  str in temp)
        end = False
        while sizes[-1]<cutOff:
            names.pop()
            sizes.pop()
            end = True
        if end:
            break
    progress=99
    yield progress
    f = open("topSubreddits.txt", "w")
    for i in range(len(names)):
        f.write(names[i]+'\t'+sfw[i]+'\t'+str(sizes[i])+'\n')
    f.close()
    progress=100
    yield progress
