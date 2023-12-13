import os
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 00d_Plot_Std_Orog_ENS_9km.py plots the standard deviation of sub-gridscale orography 
# from the new ENS (at 9 km resolution).
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the USA's mask is stored.
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
Mask_Domain = [15,-135,55,-55]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ENS_9km/Mask.grib"
DirOUT = "Data/Plot/00d_Std_Orog_ENS_9km"
###########################################################################


# Retrieving the standard deviation of sub-gridscale orography
print("Retrieving the standard deviation of sub-gridscale orography...")
sdor = mv.retrieve(
    {"class" : "od",
     "stream" : "enfo", 
     "type" : "cf", 
     "expver" : "1", 
     "levtype" : "sfc",
     "param" : "160.128",
    })

# Reading USA's domain
print("Reading the USA's domain ...")
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask = mv.bitmap(mask,0) # bitmap the values outside the domain

# Selecting the standard deviation of sub-gridscale orography values within the considered domain
print("Selecting the standard deviation of sub-gridscale orography values within the considered domain...")
sdor_mask = (mask == 1) * sdor

# Plotting the standard deviation of sub-gridscale orography values within the considered domain
print("Plotting the standard deviation of sub-gridscale orography values within the considered domain...")

geo_view = mv.geoview(
    map_projection = "mercator",
    map_area_definition = "corners",
    area = Mask_Domain
    )
    
coastlines = mv.mcoast(
    map_coastline_colour = "charcoal",
    map_coastline_thickness = 1,
    map_coastline_resolution = "high",
    map_coastline_sea_shade = "on",
    map_coastline_sea_shade_colour = "RGB(0.7398,0.9465,0.943)",
    map_boundaries = "on",
    map_boundaries_colour = "charcoal",
    map_boundaries_thickness = 1,
    map_grid_latitude_increment = 5,
    map_grid_longitude_increment = 10,
    map_label_right = "off",
    map_label_top = "off",
    map_label_colour = "charcoal",
    map_grid_thickness = 1,
    map_grid_colour = "charcoal",
    map_label_height = 0.5
    )

contouring = mv.mcont(
    legend = "on", 
    contour = "off",
    contour_level_selection_type = "level_list",
    contour_level_list = [0, 10, 25, 50, 75, 100, 250, 500, 1000, 5000],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_technique = "grid_shading",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = [
        "rgb(0.0477,0.3209,0.2253)", # 0-10
        "rgb(0,0.451,0.2941)", # 10-25
        "rgb(0.02191,0.7232,0.4777)", # 25-50
        "rgb(0.3929,0.8071,0.6621)", # 50-75
        "rgb(0.6554,0.9211,0.8237)", # 75-100
        "rgb(0.9367,0.9484,0.7143)", # 100-250
        "rgb(0.926,0.6198,0.007324)", # 250-500
        "rgb(0.5832,0.4009,0.03645)", # 500 - 1000,
        "rgb(0.8118,0.8118,0.8118)"  # 1000 - 5000
        ])

legend = mv.mlegend(
    legend_text_colour = "charcoal",
    legend_text_font_size = 0.5,
    )

title = mv.mtext(
    text_line_count = 2,
    text_line_1 = "Standard deviation of sub-gridscale orography [metres]",
    text_line_2 = " ",
    text_colour = "charcoal",
    text_font_size = 0.75
    )

# Saving the plot
print("Saving the map plot ...")
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Std_Orog" 
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, sdor_mask, contouring, coastlines, legend, title)