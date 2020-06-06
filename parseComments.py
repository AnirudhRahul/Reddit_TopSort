import zstandard as zstd
import sys
import orjson as json
from tools import subreddit_map
import numpy as np

# from numba import njit, jit, prange
# from numba.typed import List
# import warnings
# warnings.filterwarnings('ignore')

# arr = List()
# map = subreddit_map()
# size = len(map)
# RAM_USAGE = 0.5
# cache = (RAM_USAGE*8e9//(size*32))
# arr = np.zeros((size,cache), dtype=np.int32)
# end = np.zeros(size, dtype=np.int32)
# # a users reddit 'fullname'(basically their id) is just t5_ followed by a base 36 number
# # we will just keep track of the base 36 number to save space
# for i in range(len(map)):
#     arr.append(List([-1]))


# @njit
# def process(arr, fullname, rank):
#     arr[rank].append(fullname)
#
#
# @jit(parallel=True)
# def parse(chunk, prev):
#     string_data = chunk.decode('utf-8')
#     lines = string_data.split("\n")
#     # print(lines)
#     # print(lines[:-1])
#     length = len(lines)
#     for i in prange(length):
#         line = lines[i]
#         if i == 0:
#             line = prev + line
#         # try:
#         if i == length - 1:
#             continue
#         obj = json.loads(line)
#
#         if obj['subreddit'] in map:
#             process(arr, int(str(obj['author_fullname'])[
#                     3:], 36), map[obj['subreddit']][0])
#
#             # do something with the object here
#         # except:
#             # skipped+=1
#             # continue
#     return lines[-1]
    # processed+=len(lines)
    # mod+=1
    # if mod%1000==0:
    #     print(processed)

file = "RC_2019-12.zst"
tic = timer()
with open(file, 'rb') as fh:
    dctx = zstd.ZstdDecompressor()
    with dctx.stream_reader(fh) as reader:
        previous_line = ""
        processed = 0
        mod = 0
        skipped = 0
        while True
            string_data = previous_line + reader.read(65536 * 512).decode('utf-8')
            end = string_data.rindex("\n")
            string_data=string_data[:end]
            pre
            if not chunk:
                break

            # previous_line = parse(chunk, previous_line)
            processed += 1
            if(processed % 100 == 0):
                print(processed)

# for i in range(len(map)):
#     arr[i] = arr[i][1:]
# output = open("subUsage.txt", "w")
# output.write(str(arr))
# print('Skipped:' + str(skipped))
