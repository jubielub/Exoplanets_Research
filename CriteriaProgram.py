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
sheet = client.open('Estimated Sigma for K & Na').sheet1

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

# Make printing easier
np.set_printoptions(suppress=True)

def recentlyPublishedPaper(singlePlanetInfo,NaArray):
    
    dates = []

    #convert date strings into actual date values
    for i in range(len(singlePlanetInfo)):

        publishedDate = singlePlanetInfo[i][2].astype(str)
        dates.append(datetime.strptime(publishedDate,'%m/%d/%Y').date())

    mostRecentPublishDate = max(dates)
    indexOfMaxDate = dates.index(mostRecentPublishDate)

    if NaArray[indexOfMaxDate][1] >= 1:
 
        if NaArray[indexOfMaxDate][1] >= 3.0:
            
            print(singlePlanetInfo[0][0] + " has definite absorption of Na")
        
        else:
            
            print(" has potential absorption of Na")
    
    else:
        
        #step 7 work - paper concludes no detection of elements 
        if NaArray[indexOfMaxDate][1] == -1:
            
            print(singlePlanetInfo[indexOfMaxDate][0] + " has no absorption of Na")
            
        #step 8 work - paper does not deny elements presence 
        else:
        
            print("There is not enough information about " + singlePlanetInfo[indexOfMaxDate][0] + " to confirm nor deny the presence of Na.")
            
    return;



#need to fix this method - it is outputting no planets as having
#definite absorption of Na:
def determineNaAbsorption_Values(singlePlanetInfo,NaArray):
    
    # use singlePlanetInfo Array and NaArray to determine planet's Na Absorption
    
    countAbsolute = 0;
    
    countFuncCall = 0;
   
    for i in range(len(singlePlanetInfo)):
           
        if NaArray[i][1] >= 3.0:
            
            countAbsolute += 1
            
            if countAbsolute == len(singlePlanetInfo):
                
                print(singlePlanetInfo[0][0] + " has definite absorption of Na")
                            
        else:
            
            #print(singlePlanetInfo[0][0] + " does not have definite absorption of Na")
            
            if countFuncCall == 0:
                countFuncCall += 1
                recentlyPublishedPaper(singlePlanetInfo,NaArray)
                
            break;
        
           
    countPotential = 0;
    
    for i in range(len(singlePlanetInfo)):
           
        if NaArray[i][0] >= 1 and NaArray[i][1] < 3.0 and NaArray[i][1] > 1:
            
            countPotential += 1
            
            if countPotential == len(singlePlanetInfo):
                
                print(singlePlanetInfo[0][0] + " has potential absorption of Na")
                            
        else:
            
           #print(singlePlanetInfo[0][0] + " does not have potential absorption of Na")
           
           if countFuncCall == 0:
               countFuncCall += 1
               recentlyPublishedPaper(singlePlanetInfo,NaArray)
                
           break;
           
    countNoAbsorption = 0;
           
    for i in range(len(singlePlanetInfo)):
        
        if NaArray[i][1] < 1 or NaArray[i][1] == -1:
            
           countNoAbsorption += 1
            
           if countNoAbsorption == len(singlePlanetInfo):
                
                print(singlePlanetInfo[0][0] + " has no absorption of Na")
                            
        else:
            
           #print(singlePlanetInfo[0][0] + " all papers do that make the same claim that Na does not exist in the atmosphere.")
           
           if countFuncCall == 0:
               countFuncCall += 1
               recentlyPublishedPaper(singlePlanetInfo,NaArray)
                
           break;
         
           
    return;
    


def creatingNaValueArray(singlePlanetInfo):
     
    rows, cols = (len(singlePlanetInfo), 2)
    NaList = [[0.0 for i in range(cols)] for j in range(rows)] 
    
    NaArray = np.array(NaList)
    
    for i in range(len(singlePlanetInfo)):
        
        for j in range(len(singlePlanetInfo[i])):
            
            if j == 4:
        
                if singlePlanetInfo[i][j] != 'N/A': 
                
                    if singlePlanetInfo[i][j] != '0':
                    
                        NaList = singlePlanetInfo[i][j].split("-")
                            
                        NaArrayString = np.array(NaList)
                        
                        NaArray[i][0] = NaArrayString[0]
                        NaArray[i][1] = NaArrayString[1]
                        
                
                    else:
                    
                        NaArray[i][0] = 0;
                        NaArray[i][1] = 0;
                     
                else:
                    
                    NaArray[i][0] = -1;
                    NaArray[i][1] = -1;
                    
    determineNaAbsorption_Values(singlePlanetInfo,NaArray)

                        
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
        
        if  (planetDataArray[j][0] == planetNameArray[i]):
            
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
                
                creatingNaValueArray(singlePlanetInfo)
                
                break;




# Things to take into account other than the sigma values for concluding a planet's absorption of an element:
                
# The interpretation of the notes column of the Google Sheet - 
# interpreations of the figures included in the Notes column
# The instrument used to make these detections 
# If the authors state that the data is not high enough in resolution to 
# make a conclusion 
# If the papers provide data/figures with bins that are too broad (larger than 350 A)
# If there were time varying haxes, data resolution, or instrument errors



    
    
    # Dictionary that we will use to access columns of the table 
    # planetDetails = {'Planet_Name':0,
    #             'Paper':1,
    #             'Publication_Date':2,
    #             'Estimated_NA_Sigma_Lower_Bound':3,
    #             'Estimated_NA_Sigma_Higher_Bound':4,  
    #             'Estimated_K_Sigma_Lower_Bound':5,
    #             'Estimated_K_Sigma_Higher_Bound':6};


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
    
    
    
                    
    #                     #if NA sigma value is >= 3.0 sigma
    #                     #for all papers having this value
    #                     if NAArray[1] >= 3.0:
                            
    #                         if j == len(singlePlanetInfo) - 1:
                                
    #                             print(singlePlanetInfo[0][0] + "has definite absorption of NA")
                                
    #                             break;
                                
                            
    #                     #if there is a NA sigma value range but 
    #                     #higher bound is less than 3.0
    #                     #for all papers having this value
    #                     else if (NAArray[k][1] < 3.0) or (NAArray[k][1] >= 1.0):
                            
    #                         break;
                            
    #                         for k in range(len(singlePlanetInfo)):
                                
    #                             if (NAArray[k][1] < 3.0) or (NAArray[k][1] >= 1.0):
                                    
    #                                 if k == len(singlePlanetInfo) - 1:
                                        
    #                                     print(singlePlanetInfo[0][0] + "has potential absorption of NA")
                                        
    #                                     break;
                                
    #                             #look at the most recently published paper
    #                             else:
                                    
    #                                 dates = []
    #                                 indicies = []
                                    
    #                                 #convert date strings into actual date values
    #                                 for l in range(len(singlePlanetInfo)):
                                        
    #                                     dates.append(datetime.date(singlePlanetInfo[l][2])):
                                        
    #                                 mostRecentPublishDate = max(dates)
    #                                 indexOfMaxDate = dates.index(mostRecentPublishDate)
                                    
    #                                 if (planetDataArray[indexOfMaxDate][3] == 'N/A') or (planetDataArray[indexOfMaxDate][3] == '0'): 
                                    
    #                                 #does the paper confirm the element's presence?
    #                                 else if NAArray[indexOfMaxDate][1] >= 1.0:
                                             
    #                                     #does the paper cofirm element's presence is greater than 3.0 sigma?
    #                                     else if NAArray[indexOfMaxDate][1] > 3.0:
                                            
    #                                         print(singlePlanetInfo[0][0] + "has definite absorption of NA")
                                            
    #                                     else:
                                            
    #                                         print(singlePlanetInfo[0][0] + "has potential absorption of NA")
                                            
                                            
                                    
                            
    #                     else:
                            
    #                         break;
                            
    #                         for k in range(len(singlePlanetInfo)):
                                
    #                             if NAArray[k][1] < 1.0 :
                                    
    #                                 if k == len(singlePlanetInfo) - 1:
                                        
    #                                     print(singlePlanetInfo[0][0] + "has no absorption of NA")
                                        
    #                                     break;
                                    
    #                             #look at the most recently published paper
    #                             else:
                                    
                                
                                    
                                
                
    #             #if NA sigma value is N/A
    #             else:
                
    #                 break;
                    
    #                 for k in range(len(singlePlanetInfo)):
                                
    #                     if (planetDataArray[i][j] != 'N/A') or (planetDataArray[i][j] != '0'):
                        
    #                         if k == len(singlePlanetInfo) - 1:
                                
    #                             print(singlePlanetInfo[0][0] + "has no absorption of NA")
                                
    #                             break;
                        
    #                     #look at the most recently published paper
    #                     else:
        
    
    # return;
    


            

                
                



