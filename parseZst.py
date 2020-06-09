import sys
import ujson as json
import tools
from time import time
import os


def parseFile(filename, map):
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

  tic = time()
  for list in tools.readZst(filename, map):

    for l in list:
        if l:
            freq_counter[l[0]]+=1
            lines_processed+=1
        else:
            lines_skipped+=1
            # print(l)
    chunks+=1
    if chunks % (10*1000) == 0:
      print('\r'+str(round(100*chunks*chunkLen/total_bytes,2))+'%',end='')
      # print(lines_processed,lines_skipped)
      # print(freq_counter)

  toc = time()
  print('Time: '+ str(toc-tic))
  f = open('ratios/ratio_for_'+filename+'.txt','w')
  f.write(str(freq_counter))
  f.close()
