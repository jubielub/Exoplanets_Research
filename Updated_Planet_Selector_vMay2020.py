# -*- coding: utf-8 -*-
"""
File needed to execute code: Downloadable table from the HZ Gallery

Objectives:
1) Select exoplanets in a selected search scope consisting of two physical 
or orbital properties.
2) Generate a .csv file that lists exoplanets in the selected scope along 
with their physical and orbital property meansurements.
3) Plots the exoplanets in the selected search scope based on 
two properties on a scatter plot with a red box indicating the scope.
4) Allows user to save scatter plot and .csv file to personal computer. 

@authors: Shushmitha, Wynter & Paola
"""

# Import the necessary packages
import os 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib.patches as patches
import csv
import pandas as pd
import sys

# ------------------------------------------------------
# INPUTS & VARIABLES TO CHANGE:

# Write the filepath of the file with HZG data
os.chdir("...") 

# Write the name of the file with the HZG data
f = open("hzGallery.csv",'r') 

# Insert which properties/parameters you want to examine:
# parameter1 will go on the x-axis of the graph and will be the first column of the final table
parameter1 = 'Period'
# parameter2 will do on the y-axis of the graph and will be the second column of the final table
parameter2 = 'Mass'

parameter1Units = "days" #units corresponding to parameter1
parameter2Units = "Jupiter Radii" #units corresponding to parameter2

# selected search scope. Max and min values for parameter1 and parameter2
(x_min, x_max, y_min, y_max) = (0, 5, 1, 4)  # change to values you want 

# What you want to name the file with the plot to be named
output_fig = parameter1 + "_" + parameter2 + ".png"

# Create a name for an excel file which will contain an easy list of the 
# planet names in the selected search scope
new_filename = "Spring19_Planet_List.csv"  # output list of planets within those ranges

# ------------------------------------------------------

# Read code line by line:
lines = f.readlines()

# Make printing easier
np.set_printoptions(suppress=True)

# Dictionary that we will use to access columns of the table in hzGallery.csv
parameters = {'Mass':0,
           'Radius':1,
           'Period':2,
           'Ecentricity':3,  
           'Omega':4,
           'THZC':5,
           'THZ0':6,
           'TEQA':7,
           'TEQB':8,
           'TEQC':9,
           'TEQD':10}

# Create values that will be used as indices later
(parameter1a,parameter2a) = (parameters[parameter1], parameters[parameter2])
equilibriumTemp = parameters['TEQA']

# Take all the data in the table excluding the headers and set an empty array to fill later
dat = lines[1:]
arr0 = []

# Get rid of useless extras so that Python can read our data
for star in dat:
    lst = star.strip('\n').split(',')
    lst2 = [i.strip(' ') for i in lst]
    # Now turn empty values into '-1' so we only look at the planets which have actual values
    for index, j in enumerate(lst2):
        if not j:
            lst2[index] = "-1"
    # Now add our new data to our empty array        
    arr0.append(lst2)

# Turn our newly filled array into a numerical python array
arr1 = np.array(arr0)

    
#Take out the planet names from the array, so we only have the numerical data
planet_names = arr1[:,0]

# Turn the data into a float so that we can use individual points instead of an array
table = arr1[:,1:].astype(float)

# Find the planets with parameter1 and parameter2 data (which is why we turned empty values into a '-1')
no_blanks = np.where( (table[:,parameter1a] >= 0) & (table[:,parameter2a] >= 0) )

# Put the planets without blanks in their own table
final_table = table[no_blanks]
# Takes the names of the planets from the no_blank table
final_planet_names = planet_names[no_blanks]


x = final_table[:,parameter1a].tolist()
y = final_table[:,parameter2a].tolist()

# The operation below gets the indicies of the planets in the array final_table that 
# are in the selected search scope
indicis_in_parameter_space = np.where((final_table[:,parameter1a]>=x_min) 
                  & (final_table[:,parameter1a]<x_max) 
                  & (final_table[:,parameter2a]>=y_min) 
                  & (final_table[:,parameter2a]<y_max))[0].tolist()

# If the list, indicis_in_parameter_space is empty, that means that the user did not enter
# a selected search scope that is appropriate to the parameters they entered.
# Output an error message and stop the program if a wrong selected search scope is entered.
if(len(indicis_in_parameter_space) == 0):
    print("The scope you entered is not within the possible values for parameter1 and/or parameter2.")
    print("Please enter values for x_min, x_max, y_min, and y_max that are within the possible values for parameter1 and parameter2.")
    sys.exit()

# fill a new list with the elements in the final_table array that have indicis collected
# in inidicis_in_parameter 
planets_in_parameter_space = []
for n,i in enumerate(indicis_in_parameter_space):
    if ((final_table[i,parameter1a]>=x_min) & (final_table[i,parameter1a]<x_max) & (final_table[i,parameter2a]>=y_min) & (final_table[i,parameter2a]<y_max)):
        planets_in_parameter_space.append(final_table[i])
        
#copy the list made above into an array so that we can work with float values   
planets_in_parameter_space_array = np.array(planets_in_parameter_space)        

#find the x and y minimum in the selected search scope so that we can set the x-min
#and y-min the selector box on the plot (the box's lower left corner)
x_min_in_box = min(planets_in_parameter_space_array[:,parameters[parameter1]])
y_min_in_box = min(planets_in_parameter_space_array[:,parameters[parameter2]])

#find the x and y maximum in the selected search scope so that we can set the height
#and length of the box using the these values and the min_in_box values found above
x_max_in_box = max(planets_in_parameter_space_array[:,parameters[parameter1]])
y_max_in_box = max(planets_in_parameter_space_array[:,parameters[parameter2]])


# Tell python you want to save a figure
fig=plt.figure(1)

# Tell python you are about to make a plot
axes = plt.gca()


# Create the red box which will contain the planets in our search, and prioritize its order to go over the dots
box = patches.Rectangle(
        (x_min_in_box,y_min_in_box),
        x_max_in_box-x_min_in_box,
        y_max_in_box-y_min_in_box, 
        fill=False, 
        edgecolor='r', 
        linewidth=2,
        zorder = 10)

# Plot each planet as its own point, and clean it up so it is not one blob in the denser regions
plt.plot(x,y,'.',color = 'black', markersize = 2, zorder = 0)

# Add the red box to the plot
axes.add_patch(box)

# Set the axes to log-log scale to fit all of the planets easily on the same plot
axes.set_xscale('log')
axes.set_yscale('log')

# Set max and min values for axes
x_list_max = max(x)
y_list_max = max(y)

#set the limit of the axes to be a the max x and y value in the selected search scope
#--------------------
axes.set_xlim(0,x_list_max)
axes.set_ylim(0,y_list_max)
#--------------------

# Label your axes
plt.xlabel(parameter1 + " (" + parameter1Units + ")")
plt.ylabel(parameter2 + " (" + parameter2Units + ")")

# Name the plot
plt.title("All Planets in HZ Gallery with Both " + parameter1 + " and " + parameter2 + " Data")

# Fixes some weirdness with tick marks on log-log plots
for axis in [axes.xaxis, axes.yaxis]:
    axis.set_major_formatter(ScalarFormatter())

# Show the plot
plt.show()

# Save the plot as a png 
fig.savefig(output_fig, dpi=300) 


# Now, using another index, add the name, radius, and period information to our new file containing data
c = 1
pernt = [[' ','Name', 'Radius', 'Period']]
for i in indicis_in_parameter_space:
    pernt.append([c, final_planet_names[i], final_table[i,parameter2a], final_table[i,parameter1a]])
    c = c + 1
    
# This will write our data into the csv file we named previously, which will be moved to your routines folder
with open(new_filename,'w') as f:
    writer = csv.writer(f)
    writer.writerows(pernt)
    
    
# Print the planets we have picked out, and their radius/period information
print("  Planets in the Planet Box")

for_console_table = [['Name', parameter1, parameter2, 'TEQA']]
for i in indicis_in_parameter_space:
    for_console_table.append([final_planet_names[i], final_table[i, parameter1a], final_table[i,parameter2a], final_table[i,equilibriumTemp]])
    
df = pd.DataFrame(for_console_table)
print(df)
