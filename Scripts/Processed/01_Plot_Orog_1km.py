import os
import numpy as np
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 01_Plot_Orog_1km.py plots US orography at 1 km resolution. This plot is used only for 
# publication purposes. 
# Runtime: the code takes up to 2 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# City_Names (list of strings): name of the 20 most important cities in the US.
# City_Lats ( list of floats): latitudes of the 20 most important cities in the US.
# City_Lons ( list of floats): longitudes of the 20 most important cities in the US.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the US mask is stored.
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
Mask_Domain = [22,-130,52,-60]
City_Names = ["New York City","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio","San Diego","Dallas","San Jose","Austin","Jacksonville","Fort Worth","Columbus","Charlotte","Indianapolis","San Francisco","Seattle","Denver","Washington DC"]
City_Lats = [40.67,34.11,41.84,29.7407,33.54,40.01,29.46,32.81,32.79,37.3,30.31,30.33,32.75,39.99,35.2,39.78,37.77,47.62,39.77,38.91]
City_Lons = [-73.94, -118.41, -87.68, -95.4636, -112.07, -75.13, -98.51, -117.14, -96.77, -121.85, -97.75, -81.66, -97.34, -82.99, -80.83, -86.15, -122.45, -122.35, -104.87, -77.02]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_1km/Mask.grib"
DirOUT = "Data/Plot/01_Orog_1km"
###########################################################################

# Retrieve the geopotential height and converting it in metres
print("Reading the orography values...")
orog = mv.read("/home/rdx/data/climate/climate.v021/15999l_2/orog") * 1 # multiplying by 1 to eliminate the automatic scale of the values

# Reading US mask
print("Reading the US domain ...")
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask = mv.bitmap(mask,0) # bitmap the values outside the domain

# Selecting the orography values within the considered domain
print("Selecting the orography values within the domain ...")
orog_mask = (mask == 1) * orog

# Converting the list of the 20 biggest cities in the US into geopoints
cities_geo = mv.create_geo(type = "xyv",
    latitudes = np.array(City_Lats),
    longitudes = np.array(City_Lons),
    values = np.zeros(len(City_Lats))
    )

# Plotting the orography values within the considered domain
print("Plotting the orography values within the domain ...")

coastlines = mv.mcoast(
    map_coastline_colour = "charcoal",
    map_coastline_thickness = 2,
    map_coastline_resolution = "full",
    map_coastline_sea_shade = "on",
    map_coastline_sea_shade_colour = "rgb(0.665,0.9193,0.9108)",
    map_boundaries = "on",
    map_boundaries_colour = "charcoal",
    map_boundaries_thickness = 2,
    map_administrative_boundaries = "on",
    map_administrative_boundaries_countries_list = "usa",
    map_administrative_boundaries_style = "solid",
    map_administrative_boundaries_thickness = 2,
    map_administrative_boundaries_colour = "blue",
    map_grid_latitude_increment = 10,
    map_grid_longitude_increment = 20,
    map_label_right = "off",
    map_label_top = "off",
    map_label_colour = "charcoal",
    map_grid_thickness = 1,
    map_grid_colour = "charcoal",
    map_label_height = 0.7
    )

geo_view = mv.geoview(
    map_projection = "epsg:3857",
    map_area_definition = "corners",
    area = Mask_Domain,
    coastlines = coastlines
    )

contouring = mv.mcont(
    legend = "on", 
    contour = "off",
    contour_level_selection_type = "level_list",
    contour_level_list = [0, 50, 250, 500, 750, 1200, 1500, 2000, 2500, 99999],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_method = "area_fill",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = ["RGB(0.0353,0.4392,0.2235)", "RGB(0.3020,0.5725,0.2314)", "RGB(0.4298,0.7810,0.3327)", "RGB(0.9525,0.9259,0.5534)", "RGB(0.8706,0.7647,0.4235)", "RGB(0.7333,0.4706,0.1765)", "RGB(0.5882,0.2157,0.0392)", "RGB(0.4549,0.2784,0.2902)", "RGB(0.8235,0.8235,0.8235)"]
    )

symb_cities = mv.msymb(
    legend = "off",
    symbol_type = "marker",
    symbol_table_mode = "on",
    symbol_outline = "on",
    symbol_min_table = [-0.1],
    symbol_max_table = [0.1],
    symbol_colour_table = "black",
    symbol_marker_table = 17,
    symbol_height_table = 0.8
    )

legend = mv.mlegend(
    legend_text_colour = "charcoal",
    legend_text_font_size = 0.5,
    )

title = mv.mtext(
    text_line_count = 2,
    text_line_1 = "Orography [m.a.s.l.]",
    text_line_2 = " ",
    text_colour = "charcoal",
    text_font_size = 0.75
    )

# Saving the plot
print("Saving the map plot ...")
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Orog" 
png = mv.png_output(output_width = 5000, output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, orog_mask, contouring, cities_geo, symb_cities, legend, title)