
#pass the arguements 'nsfw' and 'sfw'
#leave empty to get all subreddits
def subreddit_map(type=''):
    f = open("topSubreddits.txt", "r")
    data = dict()
    index = 0
    for line in f:
        vals = line.split()
        if type=='' or vals[1]==type:
            data[vals[0]]=[index,int(vals[2])]
            index+=1
    return data


# print(subreddit_map('nsfw'))
# print(len(subreddit_map('nsfw')))
