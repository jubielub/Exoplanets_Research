# -*- coding: utf-8 -*-
"""
Files needed for program to execute: 
    
1)'Stellar, Planetary, Absorption Data' page in 
'Spring-19 Planets Stellar, Parameter, Na & K Absorption Data' Google Sheet

2)'parameterplotdata-d463b21ec310.json' file must be located in the same 
folder as this program's file

The program reads exoplanets' physical and stellar properties 
and sodium and potassium absorption data. 
It plots planets based on any two physical and/or stellar properties and 
indicates which planets have absolute, potential, and no absorption of 
sodium and/or potassium. Program saves all created plots to
indicated file path in personal computer

@authors: Shushmitha Radjaram and Wynter Broussard
"""

# Import the necessary packages
import os
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# Python API for Google Sheets:
# Allows Python program to open, read, and write to a Google Shet
import gspread 
# Ensures access is given to only users that have the json_keyfile_name
from oauth2client.service_account import ServiceAccountCredentials 


# scope: how do you want the program to interact with Google Sheet, this 
# particular link can be found on the google developer page to give different 
# level of access to people who are working with spreadsheet or other docs
scope = ["https://www.googleapis.com/auth/drive"] 


# You must make sure that 'parameterplotdata-d463b21ec310.json' is saved in 
# the same folder that this Python Program is saved
# JSON files provides the credentials to access the Google Sheet
credentials = ServiceAccountCredentials.from_json_keyfile_name('parameterplotdata-d463b21ec310.json', scope)

# Google Sheet API client now has permission to access the Google Sheet
client = gspread.authorize(credentials)

# Open Google Sheet with data and save it to the Worksheet object "sheet"
sheet = client.open('Absorption Results and Parameter Data for Plots Fall 2019').sheet1

# Save all values of object "sheet" to list that will be used for plot-making 
rawList = sheet.get_all_values()

# Save all values of object "sheet" except the headers of each column - there
# is no need to use column headers for this program
planetDataList = rawList[1:]

# ------------------------------------------------------
# INPUTS & VARIABLES TO CHANGE:

# Set strFile variable with the file path of the FOLDER 
# you want the plots to be saved to
strFile = "..."

# ------------------------------------------------------

# Turn newly filled list into a numerical python array
planetDataArray = np.array(planetDataList)

# Store planet names in different which will be later used from creating plots
planet_names = planetDataArray[0:,0]

# Dictionary that we will use to access columns of the table in Google Sheet
parameters = {'Stellar Effective Temperature':0,
            'Stellar Surface Gravity':1,
            'Stellar Metallicity':2,
            'Stellar Radius':3,  
            'Stellar Mass':4,
            'Planet Mass':5,
            'Planet Orbital Period':6,
            'Planet Equilibrium Temperature':7,
            'Planet Average Density':8,
            'Planet Radius': 9,
            'Sodium Absorption':10,
            'Potassium Absorption':11}

# Array of units that correspond to each physical and stellar property
units = ['(Kelvin)', '$(m/s^{2})$', '(dex)', '$(R_{Sun})$', '$(M_{Sun})$', '$(M_{J})$', 
         '(days)', '(K)', '$(g/cm^{3})$', '$(R_{J})$']

# Array that stores the physical and stellar properties 
# (not the element absorption data)
arrayWithValues = planetDataArray[0:,(3,4,5,6,7,9,10,11,12,13)].astype(float)

# Array with sodium absorption data
sodium = parameters['Sodium Absorption']

# Array with potassium absorption data
potassium = parameters['Potassium Absorption']

# Convert sodium and potassium arrays in to lists so we can use them later
sodium_array = planetDataArray[0:,1]
potassium_array = planetDataArray[0:,2]

# Set colors for each point representing a planet
colors = [cm.hsv(i/float(len(planet_names))) for i in range(len(planet_names))]


# makePlot function creates a plot based on the values
# for parameter1 and parameter2 in the function call
def makePlot(parameter1, parameter2):

    # Assign dictionary objects corresponding to parameter1 and parameter2 
    # parameter1 and parameter2 are physical or stellar properties of exoplanets
    (parameter1a,parameter2a) = (parameters[parameter1], parameters[parameter2])
    
    # x and y arrays correspond to the properties corresponding to 
    # parameter1 and parameter2
    x = arrayWithValues[:,parameter1a].tolist()
    y = arrayWithValues[:,parameter2a].tolist()
    
     
    # Assign variables for parameter1/x minimum and maximum 
    # and parameter2/y minimum and maximum
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    

    # 'Stellar Effective Temperature' and 'Planet Equilibrium Temperature' 
    # values are much larger than other property values, so method 
    # setUpForTempPlot is called to set up plots in a modified way that include
    # temperature values 
    if (parameter1 or parameter2 == 'Stellar Effective Temperature') or (parameter1 or parameter2 == 'Planet Equilibrium Temperature'):
        
        setUpForTempPlot(x, y)
        
    
    # if neither parameter1 nor parameter2 are Temperature 
    else:
        
        # Set dimensions of the plot
        fig, ax = plt.subplots(figsize=(10,7), dpi= 80, facecolor='w', edgecolor='k') 
    
    
        # Set the diameter of the circles drawn around points
        # represention sodium and potassium absorption
        diameter_of_Na_circle = (x_max - x_min)/30
        diameter_of_K_circle = (x_max - x_min)/45
        
        # This loop draws blue circles around points representing
        # planets based on their sodium absorption characteristic
        for i in range(len(x)):
            
            # A solid circle is drawn if a planet has absolute absorption of sodium
            if sodium_array[i] == '1':
                circle1 = patches.Circle((x[i],y[i]), diameter_of_Na_circle,linewidth=2,
                                            zorder=4.5, edgecolor='b', fill=False)
                ax.add_patch(circle1)
                
            # A dashed circle is drawn if a planet has possible absorption of sodium
            elif sodium_array[i] == '0.5':
                circle2 = patches.Circle((x[i],y[i]), diameter_of_Na_circle, edgecolor='b',
                                            zorder=4.5, linewidth=2, linestyle = '--', fill=False)
                ax.add_patch(circle2)
                
            # No circle is drawn if a planet has no absorption of sodium
            elif sodium_array[i] == '0':
                pass
            
        # This loop draws green circles around points representing
        # planets based on their potassium absorption characteristic
        for i in range(len(x)):
            
            # A solid circle is drawn if a planet has absolute absorption of potassium
            if potassium_array[i] == '1':
                circle1 = patches.Circle((x[i],y[i]), diameter_of_K_circle,linewidth=2,
                                            zorder=4.5, edgecolor='g', fill=False)
                ax.add_patch(circle1)

            # A dashed circle is drawn if a planet has possible absorption of potassium
            elif potassium_array[i] == '0.5':
                circle2 = patches.Circle((x[i],y[i]), diameter_of_K_circle, edgecolor='g',
                                            zorder=4.5, linewidth=2, linestyle = '--', fill=False)
                ax.add_patch(circle2)
                
            # No circle is drawn if a planet has no absorption of potassium
            elif potassium_array[i] == '0':
                pass
        
        
        # Set equal scaling for the axes (makes sure circles around points are circular)
        plt.axis('equal')
        

            
    # Loop sets the characteristics (coordinates, size, color, border, etc.) 
    # of individual points
    for i in range(len(x)):
        plt.scatter(x[i], y[i], s = 90, c=colors[i], 
                    label = planet_names[i], edgecolor = 'black', zorder = 3.5)
        

    # Set the width and height of grid lines     
    x_grid = (x_max - x_min)/7
    y_grid = (y_max - y_min)/7
    
    # Get plot axes to be used later
    axes = plt.gca()
    
    
    # Set the min and max x and y values the plot with have
    axes.set_xlim(x_min - x_grid, x_max + x_grid) 
    axes.set_ylim(y_min - y_grid, y_max + y_grid)
    

    # Get the corresponding units for parameter1 and parameter2 
    # from the units array
    unit1 = units[parameters.get(parameter1)]
    unit2 = units[parameters.get(parameter2)]
    

    # Set other aspects of the plot 
    plt.grid(linestyle="--", zorder=0)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.title(parameter1 + " vs " + parameter2, fontsize=16) #setting the title
    #Sets the fontsize, location on the image, and number of columns the 
    #planets are listed in
    plt.legend(fontsize=10, loc="lower center", ncol=6, bbox_to_anchor=(0.5,-0.29)) 
    

    # Sets labels for the axes based on parameter1 and parameter2
    axes.set_xlabel(parameter1 + " " + unit1, fontsize=11)
    axes.set_ylabel(parameter2 + " " + unit2, fontsize=11)

    
    # Creates a string file to save the plot NOTE: WILL ERASE PREVIOUS PLOT OF 
    # SAME NAME SO COMMENT 
    # THIS OUT/CHANGE NAME EACH TIME YOU WANT TO SAVE A PLOT
    fileSaveString = parameter1 + " vs " + parameter2 + ".png"
    if os.path.isfile(fileSaveString):
        os.remove(fileSaveString)   # Opt.: os.system("rm "+strFile)
    
    
    # Save the plot created to the file path entered for 'fileSaveString'
    # dpi sets the size of the saved .png file,
    # bbox_inches = 'tight' makes sure that the image is fit to the file
    plt.savefig(fileSaveString, dpi = (190), bbox_inches='tight')

    return;
    

# This function is used to create a plot with Temperature as one of the parameters
# Separate function is made here because
# Temperature property values are much larger than other physical property values
# and mess up the scaling of the plot elements if not accounted for separately
def setUpForTempPlot(x, y): #specify the name better!!
    
     # Set dimensions of the plot
    fig, ax = plt.subplots(figsize=(10,7), dpi= 80, facecolor='w', edgecolor='k')
    
    # Assign variables for parameter1/x minimum and maximum 
    # and parameter2/y minimum and maximum
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    
    # Set width and height of circles around points corresponding to
    # sodium and potassium absorption
    # Width and height need to be assigned because we are using ellipses
    # in the method instead of circles
    width_of_Na_circle = (x_max - x_min)/15
    width_of_K_circle = (x_max - x_min)/25
    height_of_Na_circle = (y_max - y_min)/10
    height_of_K_circle = (y_max - y_min)/15
        

    # This loop draws blue circles around points representing
    # planets based on their sodium absorption characteristic
    for i in range(len(x)):
        
        # A solid circle is drawn if a planet has absolute absorption of sodium
        if sodium_array[i] == '1':
            ellipse1 = patches.Ellipse((x[i],y[i]), width_of_Na_circle, height_of_Na_circle,linewidth=2,
                                        zorder=4.5, edgecolor='b', fill=False)
            ax.add_patch(ellipse1)
            
        # A dashed circle is drawn if a planet has possible absorption of sodium
        elif sodium_array[i] == '0.5':
            ellipse1 = patches.Ellipse((x[i],y[i]), width_of_Na_circle, height_of_Na_circle, edgecolor='b',
                                        zorder=4.5, linewidth=2, linestyle = '--', fill=False)
            ax.add_patch(ellipse1)
            
        # No circle is drawn if a planet has no absorption of sodium
        elif sodium_array[i] == '0':
            pass
    
    # This loop draws green circles around points representing
    # planets based on their potassium absorption characteristic
    for i in range(len(x)):
        
        # A solid circle is drawn if a planet has absolute absorption of potassium
        if potassium_array[i] == '1':
            ellipse1 = patches.Ellipse((x[i],y[i]), width_of_K_circle, height_of_K_circle, linewidth=2,
                                        zorder=4.5, edgecolor='g', fill=False)
            ax.add_patch(ellipse1)
            
        # A dashed circle is drawn if a planet has possible absorption of potassium        
        elif potassium_array[i] == '0.5':
            ellipse2 = patches.Ellipse((x[i],y[i]), width_of_K_circle, height_of_K_circle, edgecolor='g',
                                        zorder=4.5, linewidth=2, linestyle = '--', fill=False)
            ax.add_patch(ellipse2)
        
        # No circle is drawn if a planet has no absorption of potassium
        elif potassium_array[i] == '0':
            pass    
    
    
    return;
    

# makePlot function is called with all combinations of the parameters
# to make every plot possible using the data in Google Sheet 
    
# 40 total scatter plots:
    
# Method calls for making plots of Stellar property vs. Stellar property
makePlot('Stellar Effective Temperature', 'Stellar Surface Gravity') 
makePlot('Stellar Effective Temperature', 'Stellar Metallicity')
makePlot('Stellar Effective Temperature', 'Stellar Radius')
makePlot('Stellar Effective Temperature', 'Stellar Mass')
makePlot('Stellar Surface Gravity', 'Stellar Metallicity')
makePlot('Stellar Surface Gravity', 'Stellar Radius')
makePlot('Stellar Surface Gravity', 'Stellar Mass')
makePlot('Stellar Metallicity', 'Stellar Radius')
makePlot('Stellar Metallicity', 'Stellar Mass')
makePlot('Stellar Radius', 'Stellar Mass')

# Method calls for making plots of Physical property vs. Physical property
makePlot('Planet Average Density', 'Planet Equilibrium Temperature') 
makePlot('Planet Orbital Period', 'Planet Equilibrium Temperature')
makePlot('Planet Orbital Period', 'Planet Radius')
makePlot('Planet Orbital Period', 'Planet Mass')
makePlot('Planet Orbital Period', 'Planet Average Density')
makePlot('Planet Mass', 'Planet Equilibrium Temperature')
makePlot('Planet Mass', 'Planet Radius')
makePlot('Planet Mass', 'Planet Average Density')
makePlot('Planet Average Density', 'Planet Radius')
makePlot('Planet Radius', 'Planet Equilibrium Temperature')

# Method calls for making plots of Stellar property vs. Physical property:
 
makePlot('Stellar Effective Temperature','Planet Average Density')
makePlot('Stellar Effective Temperature', 'Planet Equilibrium Temperature')
makePlot('Stellar Effective Temperature', 'Planet Orbital Period')
makePlot('Stellar Effective Temperature', 'Planet Mass')
makePlot('Stellar Effective Temperature', 'Planet Radius')

makePlot('Stellar Surface Gravity','Planet Average Density')
makePlot('Stellar Surface Gravity', 'Planet Equilibrium Temperature')
makePlot('Stellar Surface Gravity', 'Planet Orbital Period')
makePlot('Stellar Surface Gravity', 'Planet Mass')
makePlot('Stellar Surface Gravity', 'Planet Radius')

makePlot('Stellar Metallicity','Planet Average Density')
makePlot('Stellar Metallicity', 'Planet Equilibrium Temperature')
makePlot('Stellar Metallicity', 'Planet Orbital Period')
makePlot('Stellar Metallicity', 'Planet Mass')
makePlot('Stellar Metallicity', 'Planet Radius')

makePlot('Stellar Radius','Planet Average Density')
makePlot('Stellar Radius', 'Planet Equilibrium Temperature')
makePlot('Stellar Radius', 'Planet Orbital Period')
makePlot('Stellar Radius', 'Planet Mass')
makePlot('Stellar Radius', 'Planet Radius')

makePlot('Stellar Mass','Planet Average Density')
makePlot('Stellar Mass', 'Planet Equilibrium Temperature')
makePlot('Stellar Mass', 'Planet Orbital Period')
makePlot('Stellar Mass', 'Planet Mass')
makePlot('Stellar Mass', 'Planet Radius')


