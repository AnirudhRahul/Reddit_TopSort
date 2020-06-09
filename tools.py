import array
import glob
import os
# pass the arguements 'nsfw' and 'sfw'
# leave empty to get all subreddits
def subreddit_map(type=''):
    subLists = sorted(glob.glob("subRedditList/SR_List*"))
    print("Using file: "+subLists[-1])
    #Use latest list
    f = open(subLists[-1], "r")
    data = dict()
    index = 0
    for line in f:
        vals = line.split()
        if type == '' or vals[1] == type:
            data[vals[0]] = [index, int(vals[2])]
            index += 1
    return data

import zstandard as zstd

def readZst(file, map):
  with open(file, 'rb') as fh:
      dctx = zstd.ZstdDecompressor()
      print(dctx.memory_size())
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
    name = grabFN(input)
    if sub in map:
      return (map[sub][0],name)
    else:
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
    return array.array('I',[0]*length)

if __name__ == "__main__":
    subreddit_map()
# print(subreddit_map('nsfw'))
# print(len(subreddit_map('nsfw')))
