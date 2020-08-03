import sys
import tools
import os
from os.path import join, isfile
import glob
import math
import plotly.express as px
import pandas as pd
import requests, base64
import image_tools

# Analyzes the output from parsing reddit comments
# to find out which subreddits have the most users in common

def format_base64(input):
    return 'data:image/png;base64,'+input

def retrieve_base64(url):
    return base64.b64encode(requests.get(url).content).decode('ascii')

def top_subs(outputDir, size=-1):
    output_folders = filter(os.path.isdir, glob.glob(join(outputDir,'*')))
    output_folders = list(output_folders)

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
    icons = [item['icon'].replace('&amp;','&') for item in top_list]

    default_icon = 'https://t1.rbxcdn.com/223ff07f598f4e8e803d5f594692a200'



    data = {'Name': sr_name, 'Commenters': unique_commenters, 'Subreddit Size': sr_size}
    df = pd.DataFrame(data, columns = ['Name', 'Commenters', 'Subreddit Size'])

    xlim = 5e6

    fig = px.bar(df, y="Name", x="Commenters", color="Subreddit Size",
    range_x = [0,xlim],
    color_continuous_scale='Oryel',
    orientation='h'
    )

    index = 0
    for s,link in zip(unique_commenters,icons):
        img = None
        if len(link)<1:
            img = retrieve_base64(default_icon)
        # This only exists to remove the annoying black background from AskReddit's Icon
        elif index == size - 1:
            img = image_tools.removeBG(retrieve_base64(link))
        else:
            img = retrieve_base64(link)

        img = format_base64(img)

        fig.add_layout_image(
            dict(
                source=img,
                xref="paper", yref="paper",
                x=(s/xlim)+0.2/size, y=(index/size)+0.5/size,
                sizex=0.75/size, sizey=0.75/size,
                xanchor="left", yanchor="middle"
            )
        )
        index += 1
    fig.update_yaxes(title_text='')
    fig.update_layout(
        title={
            'text': "Subreddits Ranked By # of Unique Commenters",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font = {
        'family': "Arial, monospace",
        'size': 18,
        'color': "#001177"
        }

    )

    with open('redditpost.png','wb') as f:
        f.write(fig.to_image(format="png", width=1080, height=960, scale=2))

    fig.show()
