import sys
import ujson as json
import tools
from time import time
import os
from os.path import join

# Parses reddit comments from the compressed .zst file format

def parseFile(filename, outputDir):
  # outputDir = 'output/SR_List~subreddits_Jul2020'
  map = tools.subreddit_map(name=outputDir)[0]
  lines_processed = 0
  chunks = 0
  bytes_processed = 0
  lines_skipped = 0
  chunkLen = tools.getChunkLen(filename)
  size = len(map)
  total_bytes = tools.getFileSize(filename)
  progress_factor = 9.8*chunkLen/total_bytes

  tic = time()
  # print(map)
  #Counts the number of comments made on a SR
  freq_counter = tools.makeZeros(size)
  #Tracks the ID numbesr of individual who commented on a SR
  freq_list = [[] for _ in range(size)]

  for list in tools.readZst(filename, map):
    for l in list:
        if l:
            freq_counter[l[0]]+=1
            freq_list[l[0]].append(l[1])
            lines_processed+=1
        else:
            lines_skipped+=1
    chunks+=1
    if chunks % (1000) == 0:
      print('\r',str(round(chunks*progress_factor,2)),'%',end='', sep='')

  toc = time()
  print('\nTime: '+ str(toc-tic))

  print('Lines Processed:', lines_processed)
  print('Lines Skipped:', lines_skipped)
  print('\nWriting Output to file system:', outputDir)
  comment_file= tools.grabSlice(filename,'RC','.')

  revMap = tools.rev_list(name=outputDir)[0]

  for i in range(size):
      path = join(outputDir,str(i)+'-'+revMap[i]['name'])
      os.makedirs(path, exist_ok=True)
      tools.listToFile(freq_list[i],join(path,comment_file+'.hex'))
      print('\r',i+1,'/',size,sep='',end='')

  with open(join(outputDir,'metadata.txt'),'a') as f:
      f.write(filename+'\n')
