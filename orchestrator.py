import os
import tools
import argparse
import glob

parser = argparse.ArgumentParser(
    description='This is a the orchestrator for Reddit_TopSort most of the other .py scripts can be run from here with a simple flag',
)
parser.add_argument('File',
                    metavar='file',
                    nargs='?',
                    type=str,
                    default='',
                    help='the path to comment file, should be line a line seperated json file')
parser.add_argument('-u',
                       '--update',
                       action='store_true',
                       help='update the map of subreddits')
parser.add_argument('-m',
                       '--merge',
                       action='store_true',
                       help='merge files in the output directory')
parser.add_argument('-d',
                       '--delete',
                       action='store_true',
                       help='delete files in the output directory that have already been processed')
parser.add_argument('-a',
                       '--analyze',
                       const=50,
                       default=-1,
                       type=int,
                       nargs='?',
                       help='analyze files in the output directory and calcualte adj matrix')

parser.add_argument('-g',
                       '--graph',
                       action='store_true',
                       help='graph adj_matrix')



args = parser.parse_args()

# input_path = args.File
# print(input_path)

#Must update if there are no valid lists to use
if len((glob.glob("subreddit_lists/SR_List*")))==0:
    args.update=True

if args.update:
    import create_SR_list
    print('Loading list of top subreddits with create_SR_list.py')
    create_SR_list.main()


(map, map_filename) = tools.subreddit_map()
outputDir = os.path.join('output',tools.grabSlice(map_filename,'SR_List','.'))
if args.File:
    print('Parsing Reddit Comments')
    import parseZst as p
    p.parseFile(args.File, map, outputDir)

if args.merge:
    import merge as m
    m.mergeFiles(outputDir)

if args.delete:
    import delete as d
    d.clearFiles(outputDir)

if args.analyze > 0:
    import analyze_output as a
    a.analyze(outputDir, args.analyze)

if args.graph:
    import graph as g
    g.graph(outputDir)
