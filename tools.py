import array
import glob
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

def makeZeros(length):
    return array.array('I',[0]*length)

if __name__ == "__main__":
    subreddit_map()
# print(subreddit_map('nsfw'))
# print(len(subreddit_map('nsfw')))
