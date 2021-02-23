"""
Author: Lucy McLaughlin 
Date: 19/02/2021

Acknowledgments: 
The Alan Turing Institute for funding the Newcastle Seedcorn project 
"Automating visualization", under the EPSRC grant EP/N510129/1 and for 
Nick Holliman's Turing Fellowship. 

Citation: 
"Visual Entropy and the Visualization of Uncertainty", Holliman et al, 
arXiv:1907.12879

"""

import matplotlib.pyplot as plt
from PIL import Image
import os 

# coordinate limits of available newcastle images (x=eastings), (y=northings)
x_min = 423000
x_max = 427000
y_min = 562000
y_max = 566000

def get_image(x, y, image_type, image_file):
    lowest_x = min(x)
    highest_x = max(x)
    lowest_y = min(y)
    highest_y = max(y) 

    diff_x = int(highest_x/1000) != int(lowest_x/1000)
    diff_y = int(highest_y/1000) != int(lowest_y/1000)
    extent = []
    if image_type == "newcastle":
        if (lowest_x < x_min or highest_x >= x_max or 
                lowest_y < y_min or highest_y >= y_max):
            image = "no_map.png"
        elif diff_x or diff_y:
            image = "all.png"
        else:
            x_part = str(int(lowest_x/1000))
            y_part = str(int(lowest_y/1000))
            image = x_part + y_part + ".png"
        extent = [int(x_part)*1000, int(x_part)*1000+1000, int(y_part)*1000, 
                  int(y_part)*1000+1000]
    elif image_type == "england":
        image="england_map.png"
        extent = [-6, 2, 49.9, 56]
    else:
        image=image_file
        extent=extent
    
    if image_type == "newcastle" or image_type == "england":
        dirname = os.path.split(os.path.abspath(__file__))[0]
        return "{0}/images/{1}".format(dirname,image), extent
    else:
        return image, extent

def add_image_background(filename, ax1, extent):
    im=Image.open(filename)
    asp = (im.size[1]/im.size[0])*((extent[1]-extent[0])/(extent[3]-extent[2]))
    ax1.imshow(im, extent=extent, zorder=0, aspect=asp)
    return asp