import sys
import tools
import os
from os.path import join
import glob
# Merges the output created from multiple .zst files of comments
def mergeFiles(outputDir):
    output_folders = filter(os.path.isdir, glob.glob(join(outputDir,'*')))
    output_folders = list(output_folders)
    size = len(output_folders)
    i = 1
    for folder in output_folders:
      whole_list = set()
      files = filter(lambda x:not x.startswith('completed'),os.listdir(folder))
      files = list(files)
      if len(files)>1:
          for doc in files:
            path = join(folder,doc)
            new_path = join(folder,'completed_'+doc)
            whole_list.update(tools.fileToList(path))
            if doc !='combined.hex':
                os.rename(path,new_path)
          tools.listToFile(sorted(list(whole_list)), join(folder,'combined.hex'))

      print('\r',i,'/',size,sep='',end='')
      i+=1
