<img align="left" width="100" height="100" src="https://github.com/luyc12/vizent/blob/main/vizent/example_images/vizent_logo_thumbnail.png">

# vizent

<br/>   
 
> A python library for bivariate glyphs integrated with matplotlib

This library allows the user to create visualizations using Visual Entropy Glyphs[1] as scatter points. These are bivariate glyphs which represent one value using a central colour, and a second value using an enclosing shape. The enclosing shapes have measurably varying levels of visual entropy, and a higher visual entropy corresponds to a higher value.

This library supports scatter plots on a plain background, using a cartopy map background, or using an image as a background. It is also possible to add further custom elements to your figure using matplotlib. See the examples below, or for a detailed tutorial see [medium link].

## Installation

vizent can be installed using [pip](https://pip.pypa.io/en/stable/)

```sh
pip install vizent
```
[vizent on PyPI](https://pypi.org/project/vizent)

Prerequisites:
* cartopy
* matplotlib
* numpy
* scipy
* pillow

If using Anaconda Python these will likely be included.

## Using vizent

~~~~
vizent_plot()
~~~~

>Produces a scatter plot from the provided points. Each point is displayed as a visual entropy glyph.

Parameters:

*  __x_values__ (list of floats): list of x coordinates
*  __y_values__ (list of floats): list of y coordinates
*  __colour_values__ (list of floats): list of values to be represented using colour
*  __shape_values__ (list of floats): list of values to be represented using shape
*  __size_values__ (list of floats): list of values for diameters of glyphs in points.
*  __colormap__ (colormap or registered colormap name): Optional. Use any matplotlib colormap. See [here](https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html) for full range of options. Alternatively, use "metoffice" to use the MetOffice temperature colour scheme.
*  __scale_x__ (float): Optional. Defines x size (width) of plot window in inches.
*  __scale_y__ (float): Optional. Defines y size (height) of plot window in inches. If neither scale_x nor scale_y is specified, the plot will be scaled automatically. If only one is specified, the other will be adjusted to suit the proportions of the plot.
*  __use_image__ (bool): Optional. If True, plot on an image background. This can be your own image, or certain included image background can be used, see image_type.
*  __image_type__ (str): Optional. Use one of the included image backgrounds. Use "newcastle" for detailed 3D rendering of Newcastle Upon Tyne which will be selected based on the coordinates of your points (use eastings and northings for x and y, note that a limited area is available currently), or "england" for OSM england map (use grid ref for x and y). 
*  __image_file__ (str): Optional. The image file to use as image background. 
*  __use_cartopy__ (bool): Optional. Plot the points on Cartopy map.
*  __extent__ (list of floats): Optional. If not specified, this will be generated based on the coordinates of your points such that they are all included. This is not needed when using a preset image type.
*  __scale_diverges__ (bool): Optional. If True, diverging sets of glyphs are used for positive and negative values. If not specified, your scale will diverge if both positive and negative values are included for the shape variable.
*  __shape__ (str): Optional. Glyph shape design to use for non-divergent scales. Default is sine. Available designs are:
   * "sine"
   * "saw"
   * "reverse_saw"
   * "square"
   * "triangular"
   * "concave"
   * "star"
*  __shape_pos__ (str): Optional. When using divergent scale, glyph shape design to use for positive values. Default is sawtooth. Available designs as above.
*  __shape_neg__ (str): Optional. When using divergent scale, glyph shape design to use for negative values. Default is sawtooth. Available designs as above.
*  __colour_max__ (float): Optional. Maximum value to use for colour in key.
*  __colour_min__ (float): Optional. Minimum value to use for colour in key.
*  __colour_n__ (int): Optional. Number of colour values to be shown in key.
*  __colour_spread__ (float): Optional. Total range of colour values in key. Only use if not specifying both max and min.
*  __shape_max__ (float): Optional. Maximum value to use for shape in key.
*  __shape_min__ (float): Optional. Minimum value to use for shape in key.
*  __shape_n__ (int): Optional. Number of shape values to be shown in key. If using a diverging scale, this is the number of positive values including zero. Negative values will reflect positive values.
*  __shape_spread__ (float): Optional. Total range of shape values in key. Only use if not specifying max and min.
*  __colour_label__ (str): Optional. Text label for colour values in key.
*  __shape_label__ (str): Optional. Text label for shape values in key.
*  __title__ (str): Optional. Title to display at top.
*  __x_label__ (str): Optional. Label for x axis. Not shown for image plots.
*  __y_label__ (str): Optional. Label for y axis. Not shown for image plots.
* __show_axes__ (bool): Optional. If axes are not wanted, e.g. for image plots, set to False.
*  __save__ (bool): Optional. If True, save the plot as png.
*  __file_name__ (str): Optional. If save, name of saved file.
*  __return_axes__ (bool): Optional. If True, the function will return fig, ax1. These can be used to add more MatPlotLib elements, such as lines, text boxes.
* __scale_dp__ (int): Optional. The number of decimal places that scale values should be rounded to.
* __interval_type__ (str): Optional. This defines how the shape of each glyph is determined:
  * "closest": use the closest scale value
  * "limit": use the highest scale value that the glyph value is greater than or equal to (based on modulus for negative values)
* __show_legend__ (bool): Optional. Specify whether or not to display the legend to the right of the plot.

## Glyph Designs

The available glyph shape designs are shown here in full. Value increases with frequency from left (lowest) to right (highest).

### sine
![sine glyphs](https://github.com/luyc12/vizent/blob/main/vizent/example_images/glyphs/sine.png "sine glyphs")
### saw
![saw glyphs](https://github.com/luyc12/vizent/blob/main/vizent/example_images/glyphs/saw.png "saw glyphs")
### reverse_saw
![reverse_saw glyphs](https://github.com/luyc12/vizent/blob/main/vizent/example_images/glyphs/reverse_saw.png "reverse_saw glyphs")
### square
![square glyphs](https://github.com/luyc12/vizent/blob/main/vizent/example_images/glyphs/square.png "square glyphs")
### triangular
![triangular glyphs](https://github.com/luyc12/vizent/blob/main/vizent/example_images/glyphs/triangular.png "triangular glyphs")
### concave
![concave glyphs](https://github.com/luyc12/vizent/blob/main/vizent/example_images/glyphs/concave.png "concave glyphs")
### star
![star glyphs](https://github.com/luyc12/vizent/blob/main/vizent/example_images/glyphs/star.png "star glyphs")

## Examples

### Create a basic scatterplot:

```python
from vizent import vizent_plot

x_values = [1,2,3,4,5,6,7]
y_values = [6,3,7,1,4,2,5]
colour_values = [0,3,6,9,12,15,18]
shape_values= [0,1,2,3,4,5,6]
size_values = [30,60,30,45,60,30,45]

vizent_plot(x_values, y_values, colour_values, shape_values, size_values,
            colour_label="colour", shape_label="shape",
            title="A plot with a title", x_label="This is the x axis",
            y_label="This is the y axis")
```
![scatterplot image](https://github.com/luyc12/vizent/blob/main/vizent/example_images/basic_example.png "scatterplot image")

### Create a map using Cartopy:

```python
from vizent import vizent_plot
import pandas as pd

data = pd.read_csv("englandRegions.csv")
x = data['long'].tolist()
y = data['lat'].tolist()
cases = data['dailyCases'].tolist()
accel = data['accel'].tolist()

size = [30]*len(x)
extent = [-6, 2, 49.9, 56]

vizent_plot(x, y, cases, accel, size, shape_label="Acceleration", 
            colour_label="Daily cases", use_cartopy=True, extent=extent, 
            title='COVID19 daily case count and one day acceleration \n'
            'English regions, 30th October 2020') 
```
![cartopy image](https://github.com/luyc12/vizent/blob/main/vizent/example_images/cartopy_example.png "cartopy image")

### Create a map of england using an image background:

```python
from vizent import vizent_plot
import pandas as pd

data = pd.read_csv("englandRegions.csv")
x = data['long'].tolist()
y = data['lat'].tolist()
cases = data['dailyCases'].tolist()
accel = data['accel'].tolist()

size = [30]*len(x)

vizent_plot(x, y, cases, accel, size, shape_label="Acceleration",
            colour_label="Daily cases", use_image=True,
            image_type="england", title="COVID19 daily case count and one "
            "day acceleration \n English regions, 30th October 2020")
```

![map image](https://github.com/luyc12/vizent/blob/main/vizent/example_images/england_example.png "map image")

Map is © [OpenStreetMap](https://www.openstreetmap.org/) contributors

### Use detailed background images of Newcastle Upon Tyne:

```python
from vizent import vizent_plot
import pandas as pd

data = pd.read_csv("cleaned_temp_data.csv")
eastings = data['easting'].tolist()
northings = data['northing'].tolist()
average = data['Average of Value'].tolist()
variance = data['Variance of Value'].tolist()

size = [20]*len(eastings)

vizent_plot(eastings, northings, average, variance, size, 
            "metoffice", shape_label="variance", 
            colour_label="temperature", use_image=True, 
            image_type="newcastle", colour_spread=20,
            title="Newcastle Upon Tyne Temperature Data",
            show_axes=False)
```
![newcastle image](https://github.com/luyc12/vizent/blob/main/vizent/example_images/newcastle_example.png "newcastle image")

### Add your own MatPlotLib elements to the plot:

```python
from vizent import vizent_plot
import numpy as np

# Let's take an example of a vizent plot and add to it

x = [0.05,0.35,0.75,0.9,1.35,1.55,1.85]
y = [(1 + np.sin(2 * np.pi * i)) for i in x]
colour_values = [0,3,7,2,-1,10,6]
shape_values = [1,2,3,2.3,0,3,2]
size = [30,30,30,30,30,30,30]

# Assign the output of the function to fig, ax as shown

fig, ax = vizent_plot(x, y, colour_values, shape_values, size, 
                      colormap="rainbow", shape_label="shape", 
                      colour_label="colour", return_axes=True, 
                      title="An example of adding to your plot")

# Let's add a line to the plot

t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

# Adjust zorder to control whether line is behind or in front of points, 
# background image etc. In this case, zorder=0 places the line behind the 
# points while zorder=1 would place it in front. If using a background
# image, zorder=0.5 places the line in front of the background image, 
# but behind the points.

ax.plot(t, s, zorder=0)

# Let's also add a text box with some additional information, such as the 
# data source

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
text = "Source: Some Official Data Source"

# Text box position can be adjusted

ax.text(0.05, -0.1, text, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

# And you can adjust the space around the subplot to ensure the text box
# is shown if it is outside of the axes

plt.subplots_adjust(bottom=0.15)

plt.show()
plt.close()  
```

![custom plot example](https://github.com/luyc12/vizent/blob/main/vizent/example_images/custom_example.png "custom plot example")
  

## Release History

* 1.0 First release 24/02/2021

## Meta

Author: Lucy McLaughlin

lucy.mclaughlin@newcastle.ac.uk

[vizent on github](https://github.com/luyc12/vizent)

[vizent on PyPI](https://pypi.org/project/vizent)

Distributed under the MIT license. See ``LICENSE`` for more information.

Acknowledgments: The Alan Turing Institute for funding the Newcastle Seedcorn project "Automating visualization", under the EPSRC grant EP/N510129/1 and for Nick Holliman's Turing Fellowship.

[1] "Visual Entropy and the Visualization of Uncertainty", Holliman et al, arXiv:1907.12879