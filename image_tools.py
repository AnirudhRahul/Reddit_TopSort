from PIL import Image
import PIL

def convert_file(dir):
    img = Image.open(dir)
    width, height = img.size
    icon_size = width
    divider = 1
    while icon_size>=64:
        outputDir = join(os.path.dirname(dir),'icon_'+str(icon_size)+'.webp')
        if divider != 1:
            img = img.resize((width//divider, height//divider), resample = PIL.Image.LANCZOS)
        img.save(outputDir,'WEBP')
        icon_size//=2
        divider *=2

import base64
import cv2
from io import StringIO
import numpy as np

def readb64(base64_string):
    decoded_data = base64.b64decode(base64_string)
    np_data = np.fromstring(decoded_data,np.uint8)
    img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    return img


def removeBG(base64_input):
    src = readb64(base64_input)
    src = cv2.cvtColor(src, cv2.COLOR_RGB2RGBA)


    height,width,depth = src.shape
    print(src.shape)

    mask = np.zeros((height,width), np.uint8)
    cv2.circle(mask,(width//2,height//2),width//2-2,255,thickness=-1)
    src[:, :, 3] = mask

    _, im_arr = cv2.imencode('.png', src)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    # print(base64.b64encode(im_bytes))
    # print('data:image/png;base64,'+str(base64.b64encode(im_bytes)))
    return base64.b64encode(im_bytes).decode('ascii')
