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
from .metofficelimits import *
import matplotlib
import matplotlib.cm as cm 

def scale_is_negative(values):
    return any(x<0 for x in values) and not any(x>0 for x in values)

def scale_is_divergent(values):
    return any(x<0 for x in values) and any(x>0 for x in values)

def get_colour_scale(values, max_val, min_val, n_colours, 
                     scale_spread, scale_dp):
    if scale_spread is not None and scale_spread < 0:
        scale_spread=abs(scale_spread)
    # Determine min and max scale values
    if max_val==None and min_val==None:
        if scale_spread == None:
            min_val = min(values)
            max_val = max(values)
            scale_spread = max_val - min_val
        else:
            mid_point = (min(values)+max(values))/2
            max_val = mid_point + (scale_spread/2)
            min_val = mid_point - (scale_spread/2)
    elif max_val==None:
        if scale_spread == None:
            max_val = max(values)
            scale_spread = max_val - min_val
        else:
            max_val = min_val + scale_spread
    elif min_val==None:
        if scale_spread == None:
            min_val = min(values)
            scale_spread = max_val - min_val
        else:
            min_val = max_val - scale_spread
    else:
        if min_val>=max_val:
            raise ValueError("minimum colour scale value must be lower than "
                             "maximum colour scale value")
        scale_spread = max_val - min_val
    # The user is warned if their specified values exclude data
    if min_val > min(values) or max_val < max(values):
        print("Warning: specified minimum and maximum colour scale values "
              "or specified colour scale spread exclude some data")
    # Determine intermediate values
    scale_vals = []
    for i in range(n_colours):
        try:
            scale_vals.append(np.round(min_val+scale_spread*(i/(n_colours-1)),
                                       scale_dp))
        except ZeroDivisionError:
            scale_vals.append(np.round((min_val), scale_dp))
    return scale_vals

def get_colour_mapping(colour_scale, colormap):
    if colormap == "metoffice":
        return None
    else:
        norm = matplotlib.colors.Normalize(vmin=min(colour_scale), 
                                           vmax=max(colour_scale), clip=True)
        try:
            mapping = cm.ScalarMappable(norm=norm, cmap=colormap)
        except ValueError:
            print("'{0}' is not a valid colormap. See https://matplotlib"
                  ".org/3.1.1/gallery/color/colormap_reference.html "
                  "for available colormaps. Viridis colormap will "
                  "be used by default".format(colormap))
            return cm.ScalarMappable(norm=norm, cmap="viridis")
        else:
            return mapping
    
def get_colour(value, colormap, mapping):
    if colormap == "metoffice":
        i=0
        try:
            while value > metOfficeLimits[i]:
                i += 1
        except IndexError:
            raise IndexError("Data is outside of the limits of the metoffice "
                             "scale. Select another colormap for this data.")
        return metOfficeColours[i] 
    else:
        return mapping.to_rgba(value)    

def get_shape_scale(values, max_val, min_val, n_shapes, scale_diverges, 
                    scale_spread, scale_dp):
    if scale_spread is not None and scale_spread < 0:
        scale_spread=abs(scale_spread)
    if n_shapes is not None and n_shapes > 7:
        n_shapes = 7
        print("Maximum number of shapes is 7.")
    scale_vals = []
    if n_shapes == None:
        if scale_diverges:
            n_shapes = 4
        else:
            n_shapes = 5
    
    # diverging scale
    if scale_diverges:
        if max_val==None and min_val==None:
            if scale_spread == None:
                scale_spread = 2
                max_val = max(abs(max(values, key=abs)), scale_spread/2)
                min_val = max_val * -1
            else:
                max_val = scale_spread/2
                min_val = max_val * -1
        elif max_val==None:
            if scale_spread == None:
                max_val = min_val * -1
            else:
                max_val = min_val + scale_spread
        elif min_val==None:
            if scale_spread == None:
                min_val = max_val * -1
            else:
                min_val = max_val - scale_spread
        else:
            if min_val>=max_val:
                raise ValueError("minimum shape scale value must be lower than"
                                 " maximum shape scale value")
        # -ve vals and zero
        scale_spread = 0 - min_val
        for i in reversed(range(n_shapes)):
            scale_vals.append(np.round(0-scale_spread
                                       *(i/(n_shapes-1)), scale_dp))
        # +ve values
        scale_spread = max_val
        for i in range(1, n_shapes):
            scale_vals.append(np.round(0+scale_spread
                                       *(i/(n_shapes-1)), scale_dp))
    # negative scale
    elif scale_is_negative(values): 
        if max_val==None and min_val==None:
            if scale_spread == None:
                scale_spread = 1
                max_val = max(max(values),0)
                min_val = max(abs(max(values, key=abs)), scale_spread)*-1
            else:
                max_val = 0
                min_val = -scale_spread
        elif max_val==None: 
            if scale_spread == None:
                max_val = 0
            else:
                max_val = min_val + scale_spread
        elif min_val==None:
            if scale_spread == None:
                min_val = min(values)
            else:
                min_val = max(max(values, key=abs), max_val-scale_spread, 
                              key=abs)
        else:
            if min_val>=max_val:
                raise ValueError("minimum shape scale value must be lower than"
                                 " maximum shape scale value")
        scale_spread = abs(max_val - min_val)       
        for i in reversed(range(n_shapes)):
            scale_vals.append(np.round(max_val-scale_spread
                                       *(i/(n_shapes-1)), scale_dp))
    # normal scale
    else:
        if max_val==None and min_val==None:
            if scale_spread == None:
                scale_spread = 1
                max_val = max(abs(max(values, key=abs)), scale_spread)
                min_val = min(min(values),0)
            else:
                max_val = scale_spread
                min_val = 0
        elif max_val==None:
            if scale_spread == None:
                max_val = max(abs(max(values, key=abs)), 1)
            else:
                max_val = min_val + scale_spread
        elif min_val==None:
            if scale_spread == None:
                min_val = min(min(values),0)
            else:
                min_val = max_val - scale_spread
        else:
            if min_val>=max_val:
                raise ValueError("minimum shape scale value must be lower than"
                                 " maximum shape scale value")
        scale_spread = max_val - min_val 
        for i in range(n_shapes):
            try:
                scale_vals.append(np.round(min_val+scale_spread
                                           *(i/(n_shapes-1)), scale_dp))
            except ZeroDivisionError:
                scale_vals.append(np.round((min_val), scale_dp))

    # The user is warned if their specified values exclude data
    if min_val > min(values) or max_val < max(values):
        print("Warning: specified minimum and maximum shape scale values "
              "or specified shape scale spread exclude some data")
    return scale_vals

def get_frequency_scale(shape_scale, scale_diverges):
    frequency_scale = []
    if scale_diverges:
        n_shapes = len(shape_scale)//2 + 1
        for i in reversed(range(n_shapes-1)):
            frequency_scale.append(3*(2**i))
        frequency_scale.append(0)
        for i in range(n_shapes-1):
            frequency_scale.append(3*(2**i))
    else:
        n_shapes = len(shape_scale)
        if scale_is_negative(shape_scale):
            for i in reversed(range(n_shapes-1)):
                frequency_scale.append(3*(2**i))
            frequency_scale.append(0)
        else:
            frequency_scale.append(0)
            for i in range(n_shapes-1):
                frequency_scale.append(3*(2**i))
    return frequency_scale 
            
def get_shape(value, shape=None, divergent=None, shape_pos=None, 
              shape_neg=None):
    if divergent:
        if value <= 0:
            return shape_neg
        else:
            return shape_pos
    else:
        return shape

def get_frequency(value, shape_scale, frequency_scale, interval_type):
    if len(shape_scale) == 1:
        return frequency_scale[0]
    if interval_type=="closest":
        i=0
        while value > shape_scale[i]:
            i += 1
            if i==len(shape_scale)-1:
                break
        if abs(value-shape_scale[i]) > abs(value-shape_scale[i-1]):
            i = i - 1
    elif interval_type=="limit":
        i=0
        if value <= 0:
            while value > shape_scale[i]:
                i += 1
        else:
            while value >= shape_scale[i]:
                i += 1
                if i==len(shape_scale):
                    break
            i -= 1
    else:
        raise ValueError("The specified interval type for categorizing shapes "
                         "values does not exist. Choose from 'closest' or "
                         "'limit'")
    return frequency_scale[i]