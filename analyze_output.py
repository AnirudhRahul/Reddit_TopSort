import sys
import tools
import os
from os.path import join, isfile
import numpy as np
import glob
import math

# Analyzes the output from parsing reddit comments
# to find out which subreddits have the most users in common

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
    print()

    adj_matrix = np.zeros(shape=(size,size), dtype=np.longdouble)
    coeff = np.zeros(shape=(size,size), dtype=np.longdouble)
    map = tools.rev_list()
    for i in range(size):
        print('\rCompleted output',i,end='')
        for j in range(i+1,size):
            common = len(np.intersect1d(output_data[i],output_data[j],assume_unique=True))
            if len(output_data[i])==0 or len(output_data[j])==0:
                continue
            adj_matrix[i, j] = common

    for i in range(size):
        for j in range(i+1,size):
            if len(output_data[i]) == 0 or  len(output_data[j]) == 0:
                coeff[i, j] = 0
            else:
                coeff[i, j] = map[i][1]/len(output_data[i]) * map[j][1]/len(output_data[j])

    print()
    adj_filename = 'adj_matrix_' + str(size) + '.npy'
    coeff_filename = 'coeff_matrix_' + str(size) + '.npy'

    np.save(join(outputDir, adj_filename), adj_matrix)
    np.save(join(outputDir, coeff_filename), coeff)
    print('Saved to', join(outputDir, adj_filename))

    # for (a,b) in itertools.combinations(range(size),2):
    #     print('Joe',a,b)
