#Scrape http://redditlist.com for all subreddits with over 1000 users
from lxml import html
import requests
import datetime
import argparse
import tools
import os
from os.path import join
import time

# Grabs all if the top reddits from a website with more that 100,000 users
# Creates a time stamped folder depending and creates a folder for each top subreddits found

def reportProgress(progress):
    print('\r'+str(progress)+'%', end='')

def main(cutOff=50000, prefix=''):
    names = []
    sfw = []
    sizes = []
    progress=0
    filename = 'SR_List_{:%Y-%m-%d@%H %M}'.format(datetime.datetime.now())
    filename = join('subreddit_lists/',filename+'.txt')
    print('Output Location: '+filename)
    utc =int(time.time())
    for i in range(1,50):
        page = requests.get(prefix+'http://redditlist.com/all?page='+str(i))
        reportProgress(progress)
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
    reportProgress(progress)
    f = open(filename, "w")
    f.write(str(utc)+'\n')
    for i in range(len(names)):
        f.write(names[i]+'\t'+sfw[i]+'\t'+str(sizes[i])+'\n')
    f.close()
    progress=100
    reportProgress(progress)
    print()
    map_filename = os.path.basename(filename)
    map = tools.subreddit_map(name=map_filename)[0]
    size = len(map)
    revMap = ['']*size
    for key in map:
        revMap[map[key][0]]=key
    for i in range(size):
        path = join('output',tools.grabSlice(map_filename,'SR_List','.'),str(i)+'-'+revMap[i])
        os.makedirs(path, exist_ok=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This is a Reddit Comment Scraper program',
    )
    parser.add_argument('Prefix',
                        metavar='prefix',
                        nargs='?',
                        type=str,
                        default='',
                        help='The prefix you want to use for scraping redditlist.com, this is intended to be used with the wayback machine so you can get a list from a specific date')
    args = parser.parse_args()
    main(prefix=args.Prefix)
