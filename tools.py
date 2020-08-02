import array
import glob
import os
import ujson
# pass the arguements 'nsfw' and 'sfw'
# leave empty to get all subreddits
def subreddit_map(type='', name=''):
    subLists = sorted(glob.glob("subreddit_lists/SR_List*"))
    fileToUse = subLists[-1]
    if name:
        fileToUse = [file for file in subLists if os.path.basename(name) in os.path.basename(file)][0]
    print("Using file: "+fileToUse)
    #Use latest list
    # f = open(fileToUse, "r")
    with open(fileToUse, 'r') as f:
        data = ujson.load(f)
        newMap = {}
        index = 0
        for set in data:
            set['index']=index
            newMap[set['name']]=set
            index+=1
    # index = 0
    # utc_time = None
    # for line in f:
    #     if utc_time == None:
    #         utc_time = int(line)
    #         continue
    #     vals = line.split()
    #     if type == '' or vals[1] == type:
    #         if vals[0] in data:
    #             print('DUPE '+vals[0])
    #         data[vals[0]] = [index, int(vals[2])]
    #         index += 1
        return newMap, fileToUse

def rev_list(type='', name=''):
    subLists = sorted(glob.glob("subreddit_lists/SR_List*"))
    fileToUse = subLists[-1]
    if name:
        fileToUse = [file for file in subLists if os.path.basename(name) in os.path.basename(file)][0]
    print("Using file: "+fileToUse)
    #Use latest list
    with open(fileToUse, 'r') as f:
        return ujson.load(f), fileToUse

import zstandard as zstd

def readZst(file, map):
  with open(file, 'rb') as fh:
      dctx = zstd.ZstdDecompressor()
      print('Byte Size', dctx.memory_size())
      previous_line = ""
      for chunk in dctx.read_to_iter(fh):
          lines = chunk.decode('utf-8').split("\n")
          lines[0]=previous_line+lines[0]
          previous_line=lines[-1]
          lis = [parseLine(line, map) for line in lines[:-1]]
          yield lis

def parseLine(input, map):
  try:
    sub = grabSR(input)
    user_name = grabFN(input)
    if sub in map:
      return (map[sub]['index'],user_name)
    else:
      # print(sub)
      return None
  except:
    return None

def grabSR(json):
  i=json.index("subreddit\":\"")+12
  end = json.index('\"',i)
  return (json[i:end])

def grabFN(json):
  i=json.index("author_fullname\":\"")+21
  end = json.index('\"',i)
  return int(json[i:end],36)

def getChunkLen(file):
  with open(file, 'rb') as fh:
      dctx = zstd.ZstdDecompressor()
      for chunk in dctx.read_to_iter(fh):
          return len(chunk)

def getFileSize(file):
    return os.stat(file).st_size

def makeZeros(length):
    return array.array('Q',[0]*length)

def listToFile(list,filename):
    arr = array.array('Q',list)
    f = open(filename,'wb')
    arr.tofile(f)
    f.close()

def fileToList(filename):
    pth = os.path.abspath(filename)
    sz = os.path.getsize(pth)//8
    arr = array.array('Q')
    with open(filename,'rb') as f:
        arr.fromfile(f,sz)
        return list(arr)

if __name__ == "__main__":
    subreddit_map()

def grabSlice(str, prefix, suffix):
    return str[str.index(prefix):str.index(suffix)]
# print(subreddit_map('nsfw'))
# print(len(subreddit_map('nsfw')))
