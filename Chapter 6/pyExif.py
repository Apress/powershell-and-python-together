'''
EXIF Data Acquistion
January 2019
Version 1.1
'''

'''
Copyright (c) 2019 Chet Hosmer, Python Forensics

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

'''
# Usage Example:
# fileList | python pyExif.py 
#
# Requirement: Python 3.x
#
# Requirement: 3rd Party Library that is utilized is: PILLOW
#                   pip install PILLOW  from the command line
#
# The Script will extract the EXIF/GEO data from jpeg files piped into the script
# and generate tabular list of the extracted geo locations along with a csv file
#


''' LIBRARY IMPORT SECTION '''

import os                       # Python Standard Library : Operating System Methods
import sys                      # Python Standard Library : System Methods
from datetime import datetime   # Python Standard Libary datetime method from Standard Library

# import the Python Image Library 
# along with TAGS and GPS related TAGS
# Note you must install the PILLOW Module
# pip install PILLOW

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Import the PrettyTable Library to produce tabular results
from prettytable import PrettyTable

''' EXTRACT GPS DICTIONARY SECTION '''

#
# Extract EXIF Data
#
# Input: Full Pathname of the target image
#
# Return: gps Dictionary and selected exifData list
#

def ExtractGPSDictionary(fileName):

    try:
        pilImage = Image.open(fileName)
        exifData = pilImage._getexif()

    except Exception:
        # If exception occurs from PIL processing
        # Report the 
        return None, None

    # Interate through the exifData
    # Searching for GPS Tags

    imageTimeStamp = "NA"
    cameraModel = "NA"
    cameraMake = "NA"
    gpsData = False

    gpsDictionary = {}

    if exifData:

        for tag, theValue in exifData.items():

            # obtain the tag
            tagValue = TAGS.get(tag, tag)

            # Collect basic image data if available

            if tagValue == 'DateTimeOriginal':
                imageTimeStamp = exifData.get(tag).strip()

            if tagValue == "Make":
                cameraMake = exifData.get(tag).strip()

            if tagValue == 'Model':
                cameraModel = exifData.get(tag).strip()

            # check the tag for GPS
            if tagValue == "GPSInfo":

                gpsData = True;

                # Found it !
                # Now create a Dictionary to hold the GPS Data

                # Loop through the GPS Information
                for curTag in theValue:
                    gpsTag = GPSTAGS.get(curTag, curTag)
                    gpsDictionary[gpsTag] = theValue[curTag]

        basicExifData = [imageTimeStamp, cameraMake, cameraModel]    

        return gpsDictionary, basicExifData

    else:
        return None, None

# End ExtractGPSDictionary ============================


''' EXTRACT LATTITUDE AND LONGITUDE SECTION '''

# 
# Extract the Lattitude and Longitude Values
# From the gpsDictionary
#

def ExtractLatLon(gps):

    # to perform the calcuation we need at least
    # lat, lon, latRef and lonRef
    
    try:
        latitude     = gps["GPSLatitude"]
        latitudeRef  = gps["GPSLatitudeRef"]
        longitude    = gps["GPSLongitude"]
        longitudeRef = gps["GPSLongitudeRef"]

        lat = ConvertToDegrees(latitude)
        lon = ConvertToDegrees(longitude)

        # Check Latitude Reference
        # If South of the Equator then lat value is negative

        if latitudeRef == "S":
            lat = 0 - lat

        # Check Longitude Reference
        # If West of the Prime Meridian in 
        # Greenwich then the Longitude value is negative

        if longitudeRef == "W":
            lon = 0- lon

        gpsCoor = {"Lat": lat, "LatRef":latitudeRef, "Lon": lon, "LonRef": longitudeRef}

        return gpsCoor

    except:
        return None

# End Extract Lat Lon ==============================================


''' CONVERT GPS COORIDINATES TO DEGRESS '''

# 
# Convert GPSCoordinates to Degrees
#
# Input gpsCoordinates value from in EXIF Format
#

def ConvertToDegrees(gpsCoordinate):

    d0 = gpsCoordinate[0][0]
    d1 = gpsCoordinate[0][1]
    try:
        degrees = float(d0) / float(d1)
    except:
        degrees = 0.0

    m0 = gpsCoordinate[1][0]
    m1 = gpsCoordinate[1][1]
    try:
        minutes = float(m0) / float(m1)
    except:
        minutes=0.0

    s0 = gpsCoordinate[2][0]
    s1 = gpsCoordinate[2][1]
    try:
        seconds = float(s0) / float(s1)
    except:
        seconds = 0.0

    floatCoordinate = float (degrees + (minutes / 60.0) + (seconds / 3600.0))

    return floatCoordinate

''' MAIN PROGRAM ENTRY SECTION '''

if __name__ == "__main__":
    '''
    pyExif Main Entry Point
    '''
    print("\nExtract EXIF Data from JPEG Files")
    print("Python Forensics, Inc. \n")

    print("Script Started", str(datetime.now()))
    print()

    ''' PROCESS PIPED DATA FROM POWERSHELL SECTION'''
    
    pictureList = []
    
    # Process data from standard input as a file list

    for eachLine in sys.stdin:
        entry = eachLine.strip()
        if entry:
            pictureList.append(entry)
            
    print("Processing Photos ...")
    print()

    # CDH
    # Created a mapping object

    ''' PROCESS EACH JPEG FILE SECTION '''

    latLonList = []
    
    for targetFile in pictureList:

        if os.path.isfile(targetFile):

            gpsDictionary, exifList = ExtractGPSDictionary(targetFile)
            
            if exifList:
                TS = exifList[0]
                MAKE = exifList[1]
                MODEL = exifList[2]
            else:
                TS = 'NA'
                MAKE = 'NA'
                MODEL = 'NA'

            if (gpsDictionary != None):

                # Obtain the Lat Lon values from the gpsDictionary
                # Converted to degrees
                # The return value is a dictionary key value pairs

                dCoor = ExtractLatLon(gpsDictionary)

                if dCoor:
                    lat = dCoor.get("Lat")
                    latRef = dCoor.get("LatRef")
                    lon = dCoor.get("Lon")
                    lonRef = dCoor.get("LonRef")

                    if ( lat and lon and latRef and lonRef):
                        
                        latLonList.append([os.path.basename(targetFile), '{:4.4f}'.format(lat), '{:4.4f}'.format(lon), TS, MAKE, MODEL])

                    else:
                        print("WARNING", "No GPS EXIF Data for ", targetFile)
                else:
                    continue
            else:
                continue
        else:
            print("WARNING", " not a valid file", targetFile)

    # Create Result Table Display using PrettyTable
    
    ''' GENERATE RESULTS TABLE SECTION'''
    
    ''' Result Table Heading'''
    resultTable = PrettyTable(['File-Name', 'Lat','Lon', 'TimeStamp', 'Make', 'Model'])
    
    for loc in latLonList:
        resultTable.add_row( [loc[0], loc[1], loc[2], loc[3], loc[4], loc[5] ])
    
    resultTable.align = "l" 
    print(resultTable.get_string(sortby="File-Name"))
                   
    ''' GENERATE CSV FILE SECTION '''
           
    # Create Simple CSV File Result
    with open("LatLon.csv", "w") as outFile:
        # Write Heading
        outFile.write("Name, Lat, Long\n")
    
        # Process All entries and write each line comma separated
        for loc in latLonList:
            outFile.write(loc[0]+","+loc[1]+","+loc[2]+"\n")
    
    print("LatLon.csv File Created Successfully")
    
    print("\nScript Ended", str(datetime.now()))
    print()