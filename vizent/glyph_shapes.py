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

import numpy as np
from scipy import signal

samples = 720
theta = (2 * np.pi / samples) * np.arange(0,samples) 
shape_radius = 0.8
inner_radius = 0.6
outer_radius = 1

# Various different glyph shapes
def sine_wave(freq, amp=0.18):
    r = shape_radius + (amp * np.sin(freq * theta))  
    return r    

def saw_wave(freq, direction=1, amp=0.15):
    r = 0.85 + amp * (signal.sawtooth(freq * theta, direction))
    if freq==0:
        r = [0.8]*len(r)
    return r

def reverse_saw_wave(freq, direction=0, amp=0.15):
    r = 0.85 + amp * (signal.sawtooth(freq * theta, direction))
    if freq==0:
        r = [0.8]*len(r)
    return r

def square_wave(freq, amp=0.18):
    r = 0.79 + amp * (signal.square(freq * theta))
    if freq==0:
        r = [0.8]*len(r)
    return r

def triangular_wave(freq, amp=0.18):
    r = shape_radius + amp * (signal.sawtooth(freq * theta, 0.5))
    if freq==0:
        r = [0.8]*len(r)
    return r

def concave_wave(freq, amp=0.4):
    r = 0.6 + amp * (signal.sawtooth((freq/2) * theta, 0.5)**2)
    if freq==0:
        r = [0.8]*len(r)
    return r

# function used for star glyphs
def get_line(x1, y1, x2, y2, theta):
    dx = (x2-x1)
    dy = (y2-y1)
    r = (dx*y1 - dy*x1) / ((dx * np.sin(theta)) - (dy * np.cos(theta)))
    return r

def star(freq, amp=0.15):
    r=[]
    if freq==0:
        r = 0.8 + freq*theta
    else:
        amp=0.2
        points_theta = (2 * np.pi / (2 * freq)) * np.arange(0, (2 * freq))
        points_r = 0.8 + amp * (signal.sawtooth(freq * points_theta, 0.5))

        points_x = points_r * np.cos(points_theta)
        points_y = points_r * np.sin(points_theta)

        count = 0
        for t in theta:
            try:
                if t > points_theta[count+1]:
                    count += 1
                r.append(get_line(points_x[count], points_y[count], 
                                  points_x[count+1], points_y[count+1], t))
            except:
                r.append(get_line(points_x[count], points_y[count], 
                                  points_x[0], points_y[0], t))
    return r

shapes = {"sine": sine_wave,
          "saw": saw_wave,
          "reverse_saw": reverse_saw_wave,
          "square": square_wave,
          "triangular": triangular_wave, 
          "concave": concave_wave,
          "star": star
         }

def get_shape_points(shape, frequency, direction=1):
    if shape=="saw":
        shape_points = shapes[shape](frequency, direction)
    else:
        shape_points = shapes[shape](frequency)
    x = shape_points * np.sin(theta)
    y = shape_points * np.cos(theta)
    points = np.column_stack([x,y])
    tuple_points = []
    for i in points:
        tuple_points.append(tuple(i))
    return tuple_points
