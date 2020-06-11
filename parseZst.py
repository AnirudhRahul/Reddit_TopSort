import sys
import ujson as json
import tools
from time import time
import os


def parseFile(filename, map, map_filename):
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
            # print(l)
    chunks+=1
    if chunks % (1000) == 0:
      print('\r',str(round(chunks*progress_factor,2)),'%',end='', sep='')
      # print(lines_processed,lines_skipped)
      # print(freq_counter)

  toc = time()
  print('\nTime: '+ str(toc-tic))
  baseFolder = 'output/'+tools.grabSlice(map_filename,'SR_List','.')+'/'
  print('Writing Output to file system: '+baseFolder)
  comment_file= tools.grabSlice(filename,'RC','.')

  revMap = ['']*size
  with open(baseFolder+'metadata.txt','a') as f:
      f.write(filename+'\n')
  for key in map:
    revMap[map[key][0]]=key

  for i in range(size):
      path = baseFolder+str(i)+'-'+revMap[i]
      os.makedirs(path, exist_ok=True)
      tools.listToFile(sorted(freq_list[i]),path+'/'+comment_file+'.hex')
      print('\r',i+1,'/',size,sep='',end='')
      # print(freq_list[i])
