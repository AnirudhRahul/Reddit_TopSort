import os
from time import time
import random
import struct
import array



#Optimal write size is around 10 million ints
os.remove('testFile')

tic = time()
k = 1
lis = [i for i in range(1000*k)]
f2 = open('testFile','ab')
for i in range(100):
    data = array.array('I', lis)
    data.tofile(f2)
f2.close()

toc = time()
writeTime = toc-tic

tic = time()
with open("testFile", "rb") as f:
    pth = os.path.abspath('testFile')
    sz = os.path.getsize(pth)//4
    data = array.array('I')
    data.fromfile(f,sz)
    print(data)
    # res = struct.unpack("I")
    # ls = [0]*sz
    # for i in range(sz):
    #     # if(i%1000==0):
    #     #     print(i)
    #     byte = f.read(4)
    #     ls[i] = int.from_bytes(byte,byteorder='little',signed=False)
#         print(byte)
toc = time()
readTime = toc-tic
print("WriteTime",writeTime)
print("ReadTime",readTime)
