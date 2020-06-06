import sys
import orjson as json
from tools import subreddit_map
import numpy as np
from numba import njit, jit, prange
from numba.typed import List
import warnings
warnings.filterwarnings('ignore')

arr = List()
map = subreddit_map()
size = len(map)
RAM_USAGE = 0.5
cache = (RAM_USAGE*8e9//(size*32))
arr = np.zeros((size,cache), dtype=np.int32)
end = np.zeros(size, dtype=np.int32)

def test():
  print('test')
