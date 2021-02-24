""" vizent

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
from matplotlib import gridspec
import cartopy.crs as ccrs
import cartopy.feature as cfeature 
from .glyph_shapes import shapes, get_shape_points
from .scales import * 
from .background_image import get_image, add_image_background

def add_point(x, y, shape, frequency, colour, size, ax, use_cartopy=False):
    shape_points = get_shape_points(shape,frequency)
    if use_cartopy:
        # add outer circle
        ax.scatter(x, y, marker='o', s=(size)**2, facecolor="black", 
                   linewidths=0, transform=ccrs.PlateCarree(), zorder=100)
        # add shape
        ax.scatter(x, y, marker=shape_points, 
                   s=(size*(np.abs(shape_points).max()))**2,facecolor="white", 
                   linewidths=0, transform=ccrs.PlateCarree(), zorder=101)
        # add inner circle
        ax.scatter(x, y, marker='o', s=(size*0.6)**2, facecolor=colour, 
                   linewidths=0, transform=ccrs.PlateCarree(), zorder=102) 
    else:
        # add outer circle
        ax.scatter(x, y, marker='o', s=(size)**2, facecolor="black", 
                   linewidths=0)
        # add shape
        ax.scatter(x, y, marker=shape_points, 
                   s=(size*(np.abs(shape_points).max()))**2,facecolor="white", 
                   linewidths=0)
        # add inner circle
        ax.scatter(x, y, marker='o', s=(size*0.6)**2, facecolor=colour, 
                   linewidths=0) 

def add_legend(ax2, colour_scale, colormap, colour_mapping, shape_scale, 
               frequency_scale, shape, shape_pos, shape_neg, divergent, 
               scale_x, scale_y, colour_label, shape_label):
    x_positions = [0.75,3.25]

    colour_y_positions = list(reversed(range(1, len(colour_scale)+1)))
    shape_y_positions = list(reversed(range(1, len(frequency_scale)+1)))
    ax2.set_xlim(0,5)
    ymax = max(max(colour_y_positions), max(shape_y_positions))+1
    ax2.set_ylim(0.25, ymax-0.25)
    ax2.axes.xaxis.set_visible(False)
    ax2.axes.yaxis.set_visible(False)

    y_size = (1/(2*ymax)) * scale_y
    x_size = (1/15) * scale_x
    size = (min(x_size, y_size) / 0.014)
    title_size = min(0.2*(scale_x/(max(len(str(colour_label)), 
                          len(str(shape_label)))*0.014)), (y_size/0.014))
    label_size = (0.1*(scale_x/(max(len(str(max(colour_scale))), 
                          len(str(max(shape_scale))))*0.014)))

    #add colour scale
    ax2.annotate(colour_label, (x_positions[0]+0.5, ymax-0.55), ha='center', 
                   va='center', size=title_size)
    for i in range(len(colour_y_positions)):
        ax2.scatter(x_positions[0], ymax-(i+1.25), marker='o', 
                      s=(size)**2, 
                      facecolor=get_colour(colour_scale[i],colormap,
                                           colour_mapping), 
                      linewidths=0) 
        ax2.annotate(colour_scale[i], (x_positions[0]+1.1, ymax-(i+1.25)), 
                       ha='center', va='center', size=label_size)
    #add shape scale
    ax2.annotate(shape_label, (x_positions[1]+0.5, ymax-0.55), ha='center', 
                   va='center', size=title_size)
    for i in range(len(shape_y_positions)):
        add_point(x_positions[1],ymax-(i+1.25),
        get_shape(shape_scale[i],shape,divergent,shape_pos,shape_neg),
        frequency_scale[i],(0.74902,0.74902,0.74902),size,ax2)
        ax2.annotate(shape_scale[i], (x_positions[1]+1.1, ymax-(i+1.25)), 
                       ha='center', va='center', size=label_size)

def vizent_plot(x_values, y_values, colour_values, shape_values, size_values, 
                colormap="viridis", scale_x=None, scale_y=None, 
                use_image=False, image_type=None, image_file=None, 
                use_cartopy=False, extent=None, scale_diverges=None, 
                shape="sine", shape_pos="sine", shape_neg="square", 
                colour_max=None, colour_min=None, colour_n=None, 
                colour_spread=None, shape_max=None, shape_min=None, 
                shape_n=None, shape_spread=None, colour_label="temperature", 
                shape_label="variance", title=None, x_label=None, 
                y_label=None, show_axes=True, save=False, 
                file_name="saved_plot.png", return_axes=False, 
                scale_dp=1, interval_type="closest", show_legend=True):
    """
    Draws a scatter plot of the provided points. 
    Each point is displayed as a Visual Entropy glyph. 

    Parameters:
        x_values (list of floats): list of x coordinates
        y_values (list of floats): list of y coordinates
        colour_values (list of floats): list of values to be 
                                        represented by colour
        shape_values (list of floats): list of values to be 
                                       represented by shape
        size_values (list of floats): list of values for 
                                      diameter of glyphs in 
                                      points.
        colormap (colormap or registered colormap name): 
                             Optional. Default is metoffice 
                             colour scheme. Use any matplotlib 
                             colormap.        
        scale_x (float): Optional. Defines x size of plot window
                         in inches.
        scale_y (float): Optional. Defines y size of plot window
                         in inches.       
        use_image (bool): Optional. If True, plot on an image 
                          background.        
        image_type (str): Optional. Use preset image type. 
                          "newcastle" for detailed 3d render
                          of newcastle (use eastings and
                          northings for x and y), "england" 
                          for OSM england map (use grid ref)
        image_file (str): Optional. Use any image file. Please
                          specify absolute path. You must
                          also specify the extent.
        use_cartopy (bool): Optional. Plot the points on
                            Cartopy map. 
        extent (list of floats): Optional. Axis limits or 
                                 extent of coordinates for 
                                 Cartopy. A list of four 
                                 values: [xmin, xmax, ymin, 
                                 ymax]   
        scale_diverges (bool): Optional. If True, diverging 
                               sets of glyphs are used for 
                               positive and negative values.
        shape (str): Optional. Glyph shape design to use.
                     Use shape_pos and shape_neg for 
                     divergent scale. Default is sine.
        shape_pos (str): Optional. When using divergent
                         scale, glyph shape design to use
                         for positive values.
        shape_neg (str): Optional. When using divergent
                         scale, glyph shape design to use
                         for negative values.
        colour_max (float): Optional. Maximum value to use
                            for colour in key.
        colour_min (float): Optional. Minimum value to use
                            for colour in key.
        colour_n (int): Optional. Number of colour values
                        to be shown in key.
        colour_spread (float): Optional. Total range of 
                               colour values in key. Only
                               use if not specifying max
                               and min.
        shape_max (float): Optional. Maximum value to use
                           for shape in key.
        shape_min (float): Optional. Minimum value to use
                           for shape in key.
        shape_n (int): Optional. Number of shape values
                       to be shown in key. If using a
                       diverging scale, this is the 
                       number of positive values 
                       including zero. Negative values 
                       will reflect positive values.
        shape_spread (float): Optional. Total range of 
                              shape values in key. Only
                              use if not specifying max
                              and min.
        colour_label (str): Optional. Text label for colour
                            values in key.
        shape_label (str): Optional. Text label for shape
                           values in key.
        title (str): Optional. Title for the plot.
        x_label (str): Optional. Label for x axis. Not shown 
                       for image plots.
        y_label (str): Optional. Label for y axis. Not shown 
                       for image plots.
        show_axes (bool): Optional. If axes are not wanted,
                          e.g. for image plots, set to False.
        save (bool): Optional. If True, save the plot as png.
        file_name (str): Optional. If save, name of saved file.
        return_axes (bool): Optional. If True, the function 
                            will return fig, ax1. These can be
                            used to add more MatPlotLib 
                            elements, such as lines, text 
                            boxes.
        scale_dp (int): Optional. The number of decimal places
                        that scale values should be rounded to. 
        interval_type (str): Optional. This defines how the 
                             shape of each glyph is 
                             classified:
                                "closest": use the closest 
                                           scale value
                                "limit": use the highest scale 
                                         value that the glyph 
                                         value is greater than 
                                         or equal to (based on 
                                         modulus for negative 
                                         values)
        show_legend (bool): Optional. Specify whether or not
                            to display the legend to the 
                            right of the plot.
    """
    # Check and sanitise inputs

    # lists are all of same length
    if not (len(x_values) == len(y_values) == len(colour_values) 
            == len(shape_values) == len(size_values)):
        raise ValueError("x_values, y_values, colour_values, shape_values and "
                         "size_values must all be of the same length")
    if not len(x_values) > 0:
        raise ValueError("Empty input lists")
    # lists contain only numerical values
    if not all(isinstance(i, (int, float)) for i in x_values):
        raise TypeError("x values must be numeric")
    if not all(isinstance(i, (int, float)) for i in y_values):
        raise TypeError("y values must be numeric")
    if not all(isinstance(i, (int, float)) for i in colour_values):
        raise TypeError("colour values must be numeric")
    if not all(isinstance(i, (int, float)) for i in shape_values):
        raise TypeError("shape values must be numeric")
    if not all(isinstance(i, (int, float)) for i in size_values):
        raise TypeError("size values must be numeric")

    # valid shape is specified
    if not shape in shapes:
        print("'{0}' is not a supported shape. "
              "Default will be used".format(str(shape)))
        shape="sine"
    if not shape_pos in shapes:
        print("'{0}' is not a supported shape. "
              "Default will be used".format(str(shape_pos)))
        shape_pos="sine"
    if not shape_neg in shapes:
        print("'{0}' is not a supported shape. "
              "Default will be used".format(str(shape_neg)))
        shape_neg="square"

    # scale values are numeric
    if not isinstance(scale_x, (int, float)) and not scale_x==None:
        print("scale_x must be numeric. Default will be used")
        scale_x = None
    if not isinstance(scale_y, (int, float)) and not scale_y==None:
        print("scale_y must be numeric. Default will be used")
        scale_y = None
    if scale_x is not None and scale_x <=0:
        print("scale_x must be a positive value. Default will be used.")
        scale_x = None
    if scale_y is not None and scale_y <=0:
        print("scale_y must be a positive value. Default will be used.")
        scale_y = None

    for i in [colour_min, colour_max, colour_spread, shape_min, shape_max, 
              shape_spread, colour_n, shape_n]:
        if not isinstance(i, (int, float)) and not i==None:
            raise TypeError("Scale minimum, maximum and spread values and "
                            "number of values per scale must be numerical")
    
    # if extent is not supplied, generate based on data
    if extent==None:
        if use_cartopy or use_image:
            pad = (max(max(x_values)-min(x_values), 
                       max(y_values)-min(y_values)))/10
            extent = [min(x_values)-pad, max(x_values)+pad, 
                    min(y_values)-pad, max(y_values)+pad]
    # check extent is of correct format
    elif not isinstance(extent, list):
        raise TypeError("extent must be a list of four values. Extent "
                        "should be formatted as [minimum_x, maximum_x, "
                        "minimum_y, maximum_y].")
    elif len(extent) != 4:
        raise ValueError("invalid extent. Extent should be formatted as "
                         "[minimum_x, maximum_x, minimum_y, maximum_y].")
    else:
        if (extent[0]>min(x_values) or extent[1]<max(x_values) 
            or extent[2]>min(y_values) or extent[3]<max(y_values)):
            print("Warning: specified extent excludes some data.")

    # set up subplots
    if show_legend:
        gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1]) 
    else:
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 0]) 
    fig = plt.figure()

    if use_cartopy:
        ax1 = plt.subplot(gs[0], projection=ccrs.Mercator())
        ax1.coastlines('50m', zorder=0)
        try:
            ax1.set_extent(extent)
        except ValueError:
            raise ValueError("The specified extent or values cannot be "
                             "plotted using Cartopy. Please ensure that you "
                             "are using valid latitude and longitude values. "
                             "Extent should be formatted as [minimum_x, "
                             "maximum_x, minimum_y, maximum_y].")

        ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', 
                                                     '50m', edgecolor='face', 
                                                     facecolor='#B3CFDD',
                                                     zorder=-1))
        ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                                     edgecolor='face', 
                                                     zorder=-1,
                                                     facecolor='#EFEFDB'))                                              
        gl = ax1.gridlines(draw_labels=show_axes)
        gl.xlabels_top=False
        gl.ylabels_right=False
    else:
        ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])                 

    asp=None
    if use_image:
        if image_type=="newcastle" or image_type=="england":
            extent = get_image(x_values,y_values,image_type,image_file)[1]
        try:
            asp = add_image_background(get_image(x_values,y_values, image_type, 
                                             image_file)[0], ax1, extent) 
        except:
            print("Image file not found or not valid. Figure will be created "
                  "without image background.")
            use_image=False
   
    if scale_diverges == None:
        scale_diverges = scale_is_divergent(shape_values)
    
    if colour_n == None:
        if shape_n == None:
            if scale_diverges:
                colour_n = 7
            else:
                colour_n = 5
        else:
            if scale_diverges:
                colour_n = (2*shape_n)-1
            else:
                colour_n = shape_n     
    
    # plot the points
    colour_scale = get_colour_scale(colour_values, colour_max, colour_min, 
                                    colour_n, colour_spread, scale_dp)
    colour_mapping = get_colour_mapping(colour_scale, colormap)
    shape_scale = get_shape_scale(shape_values, shape_max, shape_min, shape_n, 
                                  scale_diverges, shape_spread, scale_dp) 
    frequency_scale = get_frequency_scale(shape_scale, scale_diverges)

    for i in range(len(x_values)):
        add_point(x_values[i], 
                  y_values[i], 
                  get_shape(shape_values[i], shape, scale_diverges, shape_pos, 
                            shape_neg),
                  get_frequency(shape_values[i], shape_scale, frequency_scale, 
                                interval_type),
                  get_colour(colour_values[i], colormap, colour_mapping),
                  size_values[i], ax1, use_cartopy) 
    if extent is not None:
        if use_cartopy:
            ax1.set_extent(extent)
        else:
            ax1.set_xlim(extent[0],extent[1])
            ax1.set_ylim(extent[2],extent[3])

    # get aspect for figure scaling
    if use_cartopy:
        aspect = ((np.diff(ax2.get_xlim())[0]/(np.diff(ax2.get_ylim())[0]/2))
                  /(np.abs(np.diff(ax1.get_xlim())[0]
                                   /np.diff(ax1.get_ylim())[0])))
    elif use_image:
        aspect = ((np.diff(ax2.get_xlim())[0]/(np.diff(ax2.get_ylim())[0]/2))
                   /(np.abs(np.diff(ax1.get_xlim())[0]
                                    /np.diff(ax1.get_ylim())[0])))*asp

    # work out scaling of plot window 
    if use_cartopy or use_image:
        fig_aspect=aspect*1/2
    else:
        fig_aspect = 1
    if not show_legend:
        fig_aspect = fig_aspect*1.5
    if scale_x == None and scale_y == None:
        scale_x = 10
        scale_y = (fig_aspect * (2/3) * scale_x)
    elif scale_x == None:
        scale_x = (scale_y) / ((2/3) * fig_aspect)
    elif scale_y == None:
        scale_y = (fig_aspect * (2/3) * scale_x)
    
    fig.set_size_inches(scale_x, scale_y)

    if show_legend:
        add_legend(ax2, colour_scale, colormap, colour_mapping, shape_scale, 
                   frequency_scale, shape, shape_pos, shape_neg, 
                   scale_diverges, scale_x, scale_y, colour_label, shape_label)

    # ensure key is same height as plot
    if use_cartopy:
        aspect = ((np.diff(ax2.get_xlim())[0]/(np.diff(ax2.get_ylim())[0]/2))
                  /(np.abs(np.diff(ax1.get_xlim())[0]
                                   /np.diff(ax1.get_ylim())[0])))
        ax2.set_aspect(aspect)
    elif use_image:
        aspect = ((np.diff(ax2.get_xlim())[0]/(np.diff(ax2.get_ylim())[0]/2))
                   /(np.abs(np.diff(ax1.get_xlim())[0]
                                    /np.diff(ax1.get_ylim())[0])))*asp
        ax2.set_aspect(aspect)
    
    ax1.margins(0.1)
    plt.subplots_adjust(wspace=0.1)
    if title is not None:
        delim_title = title.split("\n")
        max_length = max(len(line) for line in delim_title)
        font_size = min(18, 1.5*(scale_x/(max_length*0.014)))
        plt.suptitle(title, fontsize=font_size, fontweight="bold")
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
        
    if not show_axes:
        ax1.axis('off') 

    fig.canvas.draw()
    plt.tight_layout()

    if not show_legend:
        ax2.axis('off')
        plt.subplots_adjust(wspace=0)

    if return_axes:
        return fig, ax1
    elif save:
        try:
            plt.savefig(file_name, dpi=500)
        except AttributeError:
            raise AttributeError("The specified file name is invalid. File "
                                 "name must be a string with or without a "
                                 "valid image file extension")
    else:
        plt.show()
    plt.close()