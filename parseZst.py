import zstandard as zstd
import sys
import ujson as json
from tools import subreddit_map,makeZeros
from time import time


def run(filter={}, filename="RC_2019-12.zst"):
  global map
  map=filter
  parseFile(filename)

def parseFile(filename):
  processed = 0
  chunks = 0
  skipped = 0
  size = len(map)

  #Counts the number of comments made on a SR
  freq_counter = makeZeros(size)

  tic = time()
  for list in readFile(filename):

    for l in list:
        if l:
            # freq_counter[l[0]]+=1
            processed+=1
        else:
            skipped+=1

    chunks+=1
    if chunks % 100 == 0:
      print(chunks)
      # print(freq_counter)
      # print(processed,skipped)
  toc = time()
  print(toc-tic)


def grabSR(json):
  i=json.index("subreddit\":\"")+12
  end = json.index('\"',i)
  return (json[i:end])

def grabFN(json):
  i=json.index("author_fullname\":\"")+21
  end = json.index('\"',i)
  return int(json[i:end],36)

def parseLine(input):
  try:
    sub = grabSR(input)
    name = grabFN(input)
    if sub in map:
      return (map[sub][0],name)
    else:
      return None
  except:
    return None

def readFile(file):
  with open(file, 'rb') as fh:
      dctx = zstd.ZstdDecompressor()
      with dctx.stream_reader(fh) as reader:
          previous_line = ""
          while True:
              # tic = time()
              chunk = reader.read(65536 * 512)
              if not chunk:
                  break
              lines = chunk.decode('utf-8').split("\n")
              lines[0]=previous_line+lines[0]
              previous_line=lines[-1]
              # toc = time()
              # print('Decode Time', toc-tic)
              # tic = time()
              lis = [parseLine(line) for line in lines[:-1]]
              yield lis
              # toc = time()
              # print('Parse Time', toc-tic)


              # previous_line = parse(chunk, previous_line)
              # processed += 1
              # if(processed % 100 == 0):
              #     print(processed)

# for i in range(len(map)):
#     arr[i] = arr[i][1:]
# output = open("subUsage.txt", "w")
# output.write(str(arr))
# print('Skipped:' + str(skipped))
