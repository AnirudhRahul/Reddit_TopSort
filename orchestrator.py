import os
import tools
import argparse
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
import scrapeList
print('Loading list of top subreddits \w scrapeList.py')
scrapeList.main()
print('Parsing Reddit Comments')

import parseZst as p
p.run(tools.subreddit_map(input_path))
