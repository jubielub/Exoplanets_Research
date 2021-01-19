# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 17:08:17 2020

@author: shush
"""

# Import the necessary packages
import os
import numpy as np
from array import array
from datetime import datetime

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
credentials = ServiceAccountCredentials.from_json_keyfile_name('research-296004-6a3d42770486.json', scope)

# Google Sheet API client now has permission to access the Google Sheet
client = gspread.authorize(credentials)

# Open Google Sheet with data and save it to the Worksheet object "sheet"
sheet = client.open('Master NA & K Absorption Results').sheet1

# Save all values of object "sheet" to list that will be used 
rawList = sheet.get_all_values()

# Save all values of object "sheet" except the headers of each column - there
# is no need to use column headers for this program
planetDataList = rawList[1:]


# ------------------------------------------------------
# INPUTS & VARIABLES TO CHANGE:

# ------------------------------------------------------

# Turn newly filled list into a numerical python array
planetDataArray = np.array(planetDataList)

# Create array with just the names of the planets in the table
planetNamesArrayRaw = planetDataArray[0:,0]

# We don't want any duplicate names to appear in the planetNameArray,
# so we must convert planetNamesArrayRaw into a list so that
# we can remove duplicate names
planetNameListRaw = planetNamesArrayRaw.tolist();
planetNameList = list(dict.fromkeys(planetNameListRaw))

# this array now has a list of all the planets we are
# analyzing and no duplicate names
planetNameArray = np.array(planetNameList)

# planetDataArray = [len(planetDataArrayRaw)][7]

# for i in range(len(planetDataArrayRaw)):
    
    
#     for j in range(len(planetDataArrayRaw[i])):
        
#         if j == 3:
            
#             if planetDataArrayRaw[i][j] != "N/A" or planetDataArrayRaw[i][j] != "0":
            
#                 NAList = planetDataArrayRaw[i][j].split("-")
                
#                 NAArray = np.array(NAList)
                
#                 planetDataArray[i][3] = NAArray[0]
                
#                 planetDataArray[i][4] = NAArray[1]
        
#         if j == 4:
            
#             if planetDataArrayRaw[i][j] != "N/A" or planetDataArrayRaw[i][j] != "0":
            
#                 KList = planetDataArrayRaw[i][j].split("-")
                
#                 KArray = np.array(KList)
                
#                 planetDataArray[i][5] = KArray[0]
                
#                 planetDataArray[i][6] = KArray[1]
                
#             else:
                
                
                
        
#         planetDataArray[i][j] = planetDataArrayRaw[i][j]
        
        
    

# Make printing easier
np.set_printoptions(suppress=True)

# Dictionary that we will use to access columns of the table 
planetDetails = {'Planet_Name':0,
            'Paper':1,
            'Publication_Date':2,
            'Estimated_NA_Sigma_Lower_Bound':3,
            'Estimated_NA_Sigma_Higher_Bound':4,  
            'Estimated_K_Sigma_Lower_Bound':5,
            'Estimated_K_Sigma_Higher_Bound':6};


def NAAbsorption(singlePlanetInfo):
     
    for i in range(len(singlePlanetInfo)):
        
        for j in range(len(singlePlanetInfo[i])):
            
            if j == 3:
        
                if (planetDataArray[i][j] != 'N/A') or (planetDataArray[i][j] != '0'):
                    
                        NAList = planetDataArray[i][j].split("-")
                            
                        NAArrayString = np.array(NAList)
                        
                        NAArray = NAArrayString.astype(np.float)
                        
                        #if NA sigma value is >= 3.0 sigma
                        #for all papers having this value
                        if NAArray[1] >= 3.0:
                            
                            if j == len(singlePlanetInfo) - 1:
                                
                                print(singlePlanetInfo[0][0] + "has definite absorption of NA")
                                
                                break;
                                
                            
                        #if there is a NA sigma value range but 
                        #higher bound is less than 3.0
                        #for all papers having this value
                        else if (NAArray[k][1] < 3.0) or (NAArray[k][1] >= 1.0):
                            
                            break;
                            
                            for k in range(len(singlePlanetInfo)):
                                
                                if (NAArray[k][1] < 3.0) or (NAArray[k][1] >= 1.0):
                                    
                                    if k == len(singlePlanetInfo) - 1:
                                        
                                        print(singlePlanetInfo[0][0] + "has potential absorption of NA")
                                        
                                        break;
                                
                                #look at the most recently published paper
                                else:
                                    
                                    dates = []
                                    indicies = []
                                    
                                    #convert date strings into actual date values
                                    for l in range(len(singlePlanetInfo)):
                                        
                                        dates.append(datetime.date(singlePlanetInfo[l][2])):
                                        
                                    mostRecentPublishDate = max(dates)
                                    indexOfMaxDate = dates.index(mostRecentPublishDate)
                                    
                                    if (planetDataArray[i][j] == 'N/A') or (planetDataArray[i][j] == '0'):
                                        
                                        
                                    
                                    #does the paper confirm the element's presence?
                                    else if NAArray[indexOfMaxDate][1] >= 1.0:
                                             
                                    
                                        #does the paper cofirm element's presence is greater than 3.0 sigma?
                                        else if NAArray[indexOfMaxDate][1] > 3.0:
                                            
                                            print(singlePlanetInfo[0][0] + "has definite absorption of NA")
                                            
                                        else:
                                            
                                            print(singlePlanetInfo[0][0] + "has potential absorption of NA")
                                            
                                            
                                    
                                    
                                        
                            
                        else:
                            
                            break;
                            
                            for k in range(len(singlePlanetInfo)):
                                
                                if NAArray[k][1] < 1.0 :
                                    
                                    if k == len(singlePlanetInfo) - 1:
                                        
                                        print(singlePlanetInfo[0][0] + "has no absorption of NA")
                                        
                                        break;
                                    
                                #look at the most recently published paper
                                else:
                                    
                                
                                    
                                
                
                #if NA sigma value is N/A
                else:
                
                    break;
                    
                    for k in range(len(singlePlanetInfo)):
                                
                        if (planetDataArray[i][j] != 'N/A') or (planetDataArray[i][j] != '0'):
                        
                            if k == len(singlePlanetInfo) - 1:
                                
                                print(singlePlanetInfo[0][0] + "has no absorption of NA")
                                
                                break;
                        
                        #look at the most recently published paper
                        else:
        
    
    return;
    

# array to store the name of the planet + how many papers written on it
# are recorded in the table
# column zero will have the name of the planet
# column 1 will have the number of papers it has
rows, cols = (len(planetNameArray), 2) 
countOfEachPlanet = [[" " for i in range(cols)] for j in range(rows)] 

# For loop to fill countOfEachPlanet array
for i in range(len(planetNameArray)):
    
    count = 0
    
    countOfEachPlanet[i][0] = planetNameArray[i]
    
    for j in range(len(planetDataArray)):
        
        if  planetDataArray[j][0] == planetNameArray[i]:
            
            count += 1
            
    countOfEachPlanet[i][1] = count;
    

# This for loop fills the array singlePlanetInfo with 
# details from the table on 1 planet and calls the NAAbsorption method
# using filled singlePlanetInto array as the argument
for i in range(len(planetNameArray)):
    
    singlePlanetInfo = []
    
    planetOccurences = 0
    
    for j in range(len(planetDataArray)):
    
        if planetDataArray[j][0] == planetNameArray[i]:
            
            singlePlanetInfo.append(planetDataArray[j])
            
            planetOccurences += 1
            
            if planetOccurences == countOfEachPlanet[i][1]:
                
                NAAbsorption(singlePlanetInfo)
                
                



