def all_subreddit_map():
    f = open("topSubreddits.txt", "r")
    data = dict()
    index = 0
    for line in f:
        vals = line.split()
        data[vals[0]]=[index,int(vals[2])]
        index+=1
    return data

def sfw_subreddit_map():
    f = open("topSubreddits.txt", "r")
    data = dict()
    index = 0
    for line in f:
        vals = line.split()
        if vals[1]=='sfw':
            data[vals[0]]=[index,int(vals[2])]
            index+=1
    return data

def nsfw_subreddit_map():
    f = open("topSubreddits.txt", "r")
    data = dict()
    index = 0
    for line in f:
        vals = line.split()
        if vals[1]=='nsfw':
            data[vals[0]]=[index,int(vals[2])]
            index+=1
    return data

print(sfw_subreddit_map())
print(len(sfw_subreddit_map()))
