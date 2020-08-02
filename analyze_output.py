import sys
import tools
import os
from os.path import join, isfile
import glob
import math
from prettytable import PrettyTable
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import statistics


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
    total_users = 430e6
    output_folders = output_folders[:size]
    output_data = [None]*size
    i = 1
    print('Loading Output into to RAM: ')
    for folder in output_folders:
        path = join(folder,'combined.hex')
        if isfile(path):
            output_data[i-1] = np.array(tools.fileToList(path), dtype=np.ulonglong)
        else:
            output_data[i-1] = np.array([], dtype=np.ulonglong)
        print('\r',i,'/',size,sep='',end='')
        i+=1
    print()

    map = tools.rev_list()[0]
    s = 0
    for i in range(size):
        s+=map[i]['size']

    print('Avg # of Reddits', s/total_users)

    t = PrettyTable(['SubReddit','# of Commenters','Size','Ratio'])
    freq = Counter()
    for i in range(size):
        t.add_row([
        output_folders[i].split('-')[-1],
        len(output_data[i]),
        map[i]['size'],
        len(output_data[i])/map[i]['size'],
        ])
    print(t)

    for i in range(size):
        freq += Counter(output_data[i])

    no_comments = total_users - sum(freq.values())
    print(no_comments)
    print(no_comments/total_users)



    # print(freq)
    # print(freq.values)
    freq = Counter(freq.values())
    # freq += Counter({0: no_comments})

    vals = []
    weights = []
    for tuple in freq.most_common():
        weights.append(tuple[1])
        vals.append(tuple[0])



    n, bins, patches = plt.hist(vals, weights = weights, facecolor='green', alpha=0.9, edgecolor='black', linewidth=1, align='left', bins=range(size))
    plt.title('Top '+str(size)+' Subreddits', fontweight='bold', fontsize='14')
    plt.ylabel('# of Redditors', color = 'red', fontsize='12', horizontalalignment='center')
    plt.xlabel('# of Subreddits User Commented In 2019',  color = 'orangered', fontsize='12', horizontalalignment='center')

    # plt.axvline(avg, color='k', linestyle='dashed', linewidth=1)
    plt.grid(which='major',axis='y', linestyle='--', alpha = 0.75)
    plt.ticklabel_format(axis='y', useMathText = True, style='scientific')
    plt.yticks([1e8, 2e8, 3e8, 4e8, 5e8],[r'$1 \times 10^8$', r'$2 \times 10^8$', r'$3 \times 10^8$', r'$4 \times 10^8$', r'$5 \times 10^8$'])
    end = min(size,int(5*size**0.5))
    plt.xlim(min(vals)-1, end)

    gap = 1
    if end>10:
        gap = 2
    if end>20:
        gap = 5
    ticks = list(range(min(vals),end+1,gap))
    # ticks[0] = 1
    plt.xticks(ticks)


    # plt.grid(True)
    plt.show()
    # print(hist_vals)


    adj_matrix = np.zeros(shape=(size,size), dtype=np.longdouble)
    coeff = np.zeros(shape=(size,size), dtype=np.longdouble)
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
                coeff[i, j] = map[i]['size']/len(output_data[i]) * map[j]['size']/len(output_data[j])

    print()
    adj_filename = 'adj_matrix_' + str(size) + '.npy'
    coeff_filename = 'coeff_matrix_' + str(size) + '.npy'

    np.save(join(outputDir, adj_filename), adj_matrix)
    np.save(join(outputDir, coeff_filename), coeff)
    print('Saved to', join(outputDir, adj_filename))

    # for (a,b) in itertools.combinations(range(size),2):
    #     print('Joe',a,b)
