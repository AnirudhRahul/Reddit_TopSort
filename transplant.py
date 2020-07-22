#Copy output from one dir to another
import argparse
import os
import glob
from os.path import join
from distutils.dir_util import copy_tree

# Moves the output for 1 SR_List to another SR_List
# can be useful if you dont want to parse the zst files multiple times

def copyOver(toDir='',fromDir=''):
    if not (toDir and fromDir):
        raise NameError('Both arguements(toDir and fromDir) are required')
    print("Retrieving files:",fromDir)
    fromFiles = getFiles(fromDir)
    print("Retrieving files:",toDir)
    toFiles = getFiles(toDir)
    for file in toFiles:
        found = [item for item in fromFiles if item[-1] == file[-1]]
        if found:
            # print('From',found[0][0])
            # print('To',file)
            copy_tree(found[0][0],file[0])
        else:
            print('No output found for',file[2],file[1],found)

    # print(getFiles(toDir))
    # print(getFiles(fromDir))


def getFiles(outputDir):
    output_folders = filter(os.path.isdir, glob.glob(join(outputDir,'*')))
    output_folders = list(output_folders)
    size = len(output_folders)
    i = 1
    out_list = []
    for folder in output_folders:
      out_list.append((folder,*os.path.basename(folder).split('-')))
      print('\r',i,'/',size,sep='',end='')
      i+=1
    print()
    return out_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Use this program to transplant output from one folder to another',
    )
    parser.add_argument('ToDir',
                        metavar='todir',
                        nargs='?',
                        type=str,
                        default='',
                        help='Output folder to import from')
    parser.add_argument('FromDir',
                    metavar='fromdir',
                    nargs='?',
                    type=str,
                    default='',
                    help='Output folder to export into')

    args = parser.parse_args()
    copyOver(toDir=args.ToDir,fromDir=args.FromDir)
