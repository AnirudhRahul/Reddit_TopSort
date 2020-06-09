import os
import tools
import argparse
import glob

parser = argparse.ArgumentParser(
    description='This is a Reddit Comment Scraper program',
)
parser.add_argument('File',
                    metavar='file',
                    type=str,
                    help='the path to comment file, should be line a line seperated json file')
parser.add_argument('-u',
                       '--update',
                       action='store_true',
                       help='update the map of subreddits')
args = parser.parse_args()

input_path = args.File
print(input_path)

#Must update if there are no valid lists to use
if len((glob.glob("subRedditList/SR_List*")))==0:
    args.update=True

if args.update:
    import scrapeList
    print('Loading list of top subreddits \w scrapeList.py')
    scrapeList.main()
print('Parsing Reddit Comments')

import parseZst as p
p.parseFile(input_path, tools.subreddit_map())
