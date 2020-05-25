def subreddit_map():
    f = open("topSubreddits.txt", "r")
    data = dict()
    index = 0
    for line in f:
        vals = line.split()
        data[vals[0]]=[index,int(vals[1])]
        index+=1
    return data

print(subreddit_map())
