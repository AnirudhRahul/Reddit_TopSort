import sys
import ujson as json
import tools
from time import time
import os
from os.path import join


def parseFile(filename, map, outputDir):
  lines_processed = 0
  chunks = 0
  bytes_processed = 0
  lines_skipped = 0
  chunkLen = tools.getChunkLen(filename)
  size = len(map)
  total_bytes = tools.getFileSize(filename)
  print('TOTAL '+str(total_bytes))
  #Counts the number of comments made on a SR
  freq_counter = tools.makeZeros(size)
  freq_list = [[] for _ in range(size)]
  tic = time()
  progress_factor = 9.8*chunkLen/total_bytes
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
      # print(lines_processed,lines_skipped)
      # print(freq_counter)

  toc = time()
  print('\nTime: '+ str(toc-tic))
  print('Writing Output to file system: '+outputDir)
  comment_file= tools.grabSlice(filename,'RC','.')

  revMap = ['']*size
  for key in map:
    revMap[map[key][0]]=key

  for i in range(size):
      path = join(outputDir,str(i)+'-'+revMap[i])
      os.makedirs(path, exist_ok=True)
      tools.listToFile(freq_list[i],join(path,comment_file+'.hex'))
      print('\r',i+1,'/',size,sep='',end='')

  with open(join(outputDir,'metadata.txt'),'a') as f:
      f.write(filename+'\n')
