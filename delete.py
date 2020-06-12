import sys
import tools
import os
from os.path import join
import glob

def clearFiles(outputDir):
    output_folders = filter(os.path.isdir, glob.glob(join(outputDir,'*')))
    output_folders = sorted(list(output_folders))
    size = len(output_folders)
    i = 1
    for folder in output_folders:
      for doc in os.listdir(folder):
        path = join(folder,doc)
        #Clear contents of file if it has been processed
        if doc.startswith('completed'):
            open(path, 'w').close()
        if doc == 'completed_combined.hex':
            os.remove(path)

      print('\r',i,'/',size,sep='',end='')
      i+=1