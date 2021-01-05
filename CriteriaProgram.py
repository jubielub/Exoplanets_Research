# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 17:08:17 2020

@author: shush
"""

# Import the necessary packages
import os
import numpy as np
from array import array


# ------------------------------------------------------
# INPUTS & VARIABLES TO CHANGE:

os.chdir("C:\\Users\\shush\\OneDrive\\Exoplanets\\Criteria_Program\\Data") 
# Write the filepath of the file with HZG data
f = open("Absorption_Results.csv",'r') # Write the name of the file with the HZG data

# ------------------------------------------------------

# Read code line by line:
lines = f.readlines()

# Make printing easier
np.set_printoptions(suppress=True)

# Dictionary that we will use to access columns of the table in hzGallery.csv
planetDetails = {'Planet_Name':0,
           'Paper':1,
           'Publication_Date':2,
           'Estimated_Na_Sigma_Value':3,  
           'Estimated_K_Sigma_Value':4}

# Take all the data in the table excluding the headers and set an empty array to fill later
dat = lines[1:]
list0 = []


# Get rid of useless extras so that Python can read our data
for star in dat:
    lst = star.strip('\n').split(',')
    lst2 = [i.strip(' ') for i in lst]
    # Now turn empty values into '-1' so we only look at the planets which have actual values
    for index, j in enumerate(lst2):
        if not j:
            lst2[index] = "-1"
    # Now add our new data to our empty array        
    list0.append(lst2)

arr0 = np.array(list0)
    
#right now - the last two numbers from the paper section are their own
#separate values - make sure to add index 1,2,3 together to be a full string 
    
#if index is 2 or 3- add it to 1 w/ a comma
#after loop, delete 2 and 3 indexes
    
# for row in arr0:
    
#     for cell in row:
        
#         print(cell, end = ' ')
    
# for row in arr0:
    
#     for cell in row:
        
#         if(cell == 2 or cell == 3):
            
#             arr0[row, 1].add("," + arr0[row, cell])
            

# np.delete(arr0, 2, 1)      
# np.delete(arr0, 3, 1)
    
#put this in a method  

 

#method for criteria
def NAAbsorption(singlePlanetInfo):
    
   
    NAValue = singlePlanetInfo[1]
    
    similar = 0
    
    if singlePlanetInfo[1][5] != 'N/A' or singlePlanetInfo[1][5] != '0':
    
        NAValue = singlePlanetInfo[1][5].split()
    
    for j in range(len(singlePlanetInfo[1:])):
        
        NAtempArray = []
        
        if singlePlanetInfo[j][5] != 'N/A' or singlePlanetInfo[j][5] != '0':
        
            #split string into the two values
            NAtempArray = singlePlanetInfo[j][5].split()
            
            if NAtempArray[1] == NAValue[1]:
            
                similar++
                continue
            
            else:
                
                print("Papers on this planet do not conclude the same absorption.")
                break
        else:
            
            if NAValue = singlePlanetInfo[j][5]:
                
                similar++
                continue
            
        else:
            
            print("Papers on this planet do not conclude the same absorption.")
            break
        
        
    if similar == len(singlePlanetInfo):
        
        #check if it part of range is 3.0
        
        #check if range is 1-2.9
        
        #check if value is N/A or 0
        
        
        
        
            
        
                
                
                
            
                
            
                
    
    
    absorptionValues = []
    
    for i in range(len(singlePlanetInfo)):
        
        if singlePlanetInfo[i][5] != 'NA' or singlePlanetInfo[i][5] != '0':
            
            #split string into the two values
            singlePlanetInfo[i][5].split()
        
    
    for j in range(len(singlePlanetInfo)):
        
        print(singlePlanetInfo[j])
        
        
    
    # #use for loop
    # for i in range(len(singlePlanetInfo)):
        
    #     Paper = singlePlanetInfo[i][1];
    #     NAValue = singlePlanetInfo[i][5];
        
    #     for j in range(len(singlePlanetInfo[1:])):
            
       

    return;  
    
    
planetName = arr0[0][0]

singlePlanetInfo = [] 

singlePlanetInfo.append(arr0[0])

for i in range(len(arr0[1:])):
    
    if planetName == arr0[i][0]:
            
        singlePlanetInfo.append(arr0[i])
        
    else:
        
        break

#call method for criteria determination
NAAbsorption(singlePlanetInfo)



