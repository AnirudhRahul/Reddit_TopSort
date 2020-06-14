import sys
import tools
import os
from os.path import join, isfile
import numpy as np
import glob
import itertools

def extract_index(path):
    str=os.path.split(path)[1]
    str = str[:str.index('-')]
    return int(str)

def analyze(outputDir, size=-1):
    output_folders = filter(os.path.isdir, glob.glob(join(outputDir,'*')))
    output_folders = list(output_folders)
    output_folders = sorted(output_folders, key = extract_index)
    if size<0:
        size = len(output_folders)
    output_folders = output_folders[:size]

    output_data = [None]*size
    i = 1
    print('Loading Output into to RAM: ')
    for folder in output_folders:
      path = join(folder,'combined.hex')
      if isfile(path):
        output_data[i-1] = np.array(tools.fileToList(path), dtype=np.ulonglong)
      else:
          print('No data for', folder)
      print('\r',i,'/',size,sep='',end='')
      i+=1
    total_len=0
    for arr in output_data:
        total_len+=arr.size
    print()
    print(format(total_len,"5.3E"))

    # adj_matrix = np.array((size,size), dtype=np.longdouble)
    # for i in range(size):
    #     for j in range(i+1,size):
    #         print(i,j)
    # for (a,b) in itertools.combinations(range(size),2):
    #     print('Joe',a,b)
