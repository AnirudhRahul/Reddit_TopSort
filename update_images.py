import sys
import tools
import os
from time import sleep
from os.path import join
import glob
import urllib.request, json
import html
import image_tools

# Clears all the files in a SR_List output directory
# without affecting the file structure
def load_images(outputDir):
    output_folders = list(filter(os.path.isdir, glob.glob(join(outputDir,'*'))))
    size = len(output_folders)

    image_folder = 'images'

    i = 1
    for folder in output_folders:
        name = folder.split('-')[-1]
        dir = join(image_folder, name)
        if not os.path.isdir(dir):
            os.mkdir(dir)

        # print(name)
        req = urllib.request.Request(
            "http://reddit.com/r/"+name+"/about.json",
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        while True:
            try:
                with urllib.request.urlopen(req) as url:
                    data = json.loads(url.read().decode())['data']
                    icon_url = ''
                    options = []
                    if 'icon_img' in data:
                        options.append(data['icon_img'])
                    if 'community_icon' in data:
                        options.append(data['community_icon'])
                    options = [o for o in options if (type(o)==str and len(o)>5)]
                    if len(options)==0:
                        break

                    icon_url = html.unescape(options[0])
                    if len(icon_url)<8:
                        break

                    file_ending = icon_url.split('?')[0].split('.')[-1]
                    icon_dir = join(dir,'icon.'+file_ending)
                    urllib.request.urlretrieve(icon_url, icon_dir)
                    image_tools.convert_file(icon_dir)

                    # print((name,os.stat(join(dir,'icon.'+file_ending)).st_size,icon_url))

                sleep(0.5)
                break
            except urllib.error.HTTPError as e:
                break
        print('\r',i,'/',size,sep='',end='')
        i+=1
    # print(os.path.basename(outputDir))
