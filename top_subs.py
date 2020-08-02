import sys
import tools
import os
from os.path import join, isfile
import glob
import math
import plotly.express as px
import pandas as pd

# Analyzes the output from parsing reddit comments
# to find out which subreddits have the most users in common

def top_subs(outputDir, size=-1):
    output_folders = filter(os.path.isdir, glob.glob(join(outputDir,'*')))
    output_folders = list(output_folders)
    # output_folders = output_folders[:20]

    if size<0:
        size = len(output_folders)

    map = tools.subreddit_map()[0]

    i = 1
    print('Loading Output : ')
    for folder in output_folders:
        path = join(folder,'combined.hex')
        name = folder.split('-')[-1]
        if isfile(path):
            map[name]['commenters'] = len(tools.fileToList(path))
        print('\r',i,'/',len(output_folders),sep='',end='')
        i+=1
    print()

    top_list = list(map.values())

    top_list.sort(key=lambda x: x['commenters'], reverse=True)
    top_list = top_list[:size]
    top_list.reverse()

    unique_commenters = [item['commenters'] for item in top_list]
    sr_name = [item['name'] for item in top_list]
    sr_size = [item['size'] for item in top_list]

    data = {'Name': sr_name, 'Commenters': unique_commenters, 'Subreddit Size': sr_size}
    df = pd.DataFrame(data, columns = ['Name', 'Commenters', 'Subreddit Size'])

    fig = px.bar(df, y="Name", x="Commenters", color="Subreddit Size",
    range_x = [0,5e6],
    color_continuous_scale='Oryel',
    orientation='h'
    )

    fig.update_layout(
        title={
            'text': "Subreddits Ranked By # of Unique Commenters",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font = {
        'family': "Caslon, monospace",
        'size': 18,
        'color': "#001177"
        }

    )

    fig.show()
