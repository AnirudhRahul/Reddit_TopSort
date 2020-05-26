import zstandard as zstd
import sys
import orjson as json
from tools import subreddit_map
import numpy as np
from numba import njit
from numba.typed import List

arr = List()
map = subreddit_map()
#a users reddit 'fullname'(basically their id) is just t5_ followed by a base 36 number
#we will just keep track of the base 36 number to save space
for i in range(len(map)):
    arr.append(List([-1]))



@njit
def process(arr, fullname, rank):
    arr[rank].append(fullname)



file = "RC_2019-12.zst"

with open(file, 'rb') as fh:
    dctx = zstd.ZstdDecompressor()
    with dctx.stream_reader(fh) as reader:
        previous_line = ""
        processed=0
        mod=0
        skipped=0
        while True:
            chunk = reader.read(65536)
            if not chunk:
                break
            string_data = chunk.decode('utf-8')
            lines = string_data.split("\n")
            for i, line in enumerate(lines[:-1]):
                if i == 0:
                    line = previous_line + line
                try:
                    obj = json.loads(line)
                    if obj['subreddit'] in map:
                        process(arr, int(str(obj['author_fullname'])[3:],36), map[obj['subreddit']][0])
                    # do something with the object here
                except:
                    skipped+=1
                    continue
            previous_line = lines[-1]
            processed+= len(lines)
            mod+=1
            if mod%100==0:
                print(processed)

output = open("subUsage.txt", "w")
output.write(str(arr))
print('Skipped:'+str(skipped))
sys.exit()
