import os
import tools
import glob

# import scrapeList
# print('Loading list of top subreddits')
# for i in scrapeList.main():
#     print(i,'%',end='\r')
print('Parsing Reddit Comments')

import parseZst as p
p.run(tools.subreddit_map())
