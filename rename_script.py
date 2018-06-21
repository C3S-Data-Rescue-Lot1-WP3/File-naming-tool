#!/usr/bin/env python
#__author__ = "Jesse David Dinneen"
#__email__ = ""jesse.dinneen@mail.mcgill.ca""
#__status__ = "prototype" 

#workflow:
##1. put copy of script.py into parent folder of images to be scanned
##2. set the values below for the current batch of images (reel, ledger type, dimensions of handwritten date in image, etc) -- including date assumptions further below if needed (images and days per date range)
##3. run script (e.g., 'python script.py') -- **caution**: it will delete any pre-existing crops folders and results.html, results.csv files
##4. View HTML table to find first image file containing a crop with a handwritten date that didn't follow the expected daterange pattern, put that file aside
##5. Repeat 3+4 until all dates match in HTML table - can delete crops folder and results.html file afterwards if unwanted
##6. Manually insert the set aside files into CSV file

#import libaries - all but PIL are included in a normal python installation
import os
import datetime
import csv
import shutil
from PIL import Image ##for image manipulation

#set the values for the current batch
reel = "1"
item = "1"
ledger = "A"
imagefolder = 'images'
cropdimensions = (1700,  180,  2550,  360)
start = datetime.date(1874, 8, 1)
spacer = "_" ##used in new file names

#prepare HTML output
htmlstart="<!DOCTYPE html><html><head><title>Results</title></head><body>"
htmltablestring="<table border=\"1\">"
htmltablestring += "<tr><td>File</td><td>Start date</td><td>End date</td><td>Image crop</td></tr>" ##html table 1st row (colum names)
htmlend="</body></html>"

#prepare CSV output ('rows' list)
rows = []
rows.append(["Reel",  "Item",  "File",  "New file",  "Start date", "End date",  "Ledger type"]) ##CSV 1st row (column names)

#cleanup the script's folder: delete any 'crops' folders, results.html and results.csv files
if (os.path.isdir('crops') & os.path.exists('crops')):
    shutil.rmtree('crops')
    os.mkdir('crops')
else:
    os.mkdir('crops')
if os.path.exists('results.html'):
    os.unlink('results.html')
if os.path.exists('results.csv'):
    os.unlink('results.csv')

#for each image in images folder: guess dates, save a crop from image, save info into rows[] and HTML table
counter1 = 0
for file in sorted(os.listdir(imagefolder)):
    if '.' in file:
        splitname = file.rsplit('.', 1)
        if splitname[1] in ["jpg",  "JPG"]:
            thisrow = ""
            ##following 'if block' assumes: 2 images and 3 days per date range
            if counter1 == 0: ##happens only on first image found 
                counter1 += 1
            elif counter1 == 1: ##increment counter (to 2)
                counter1 += 1
            elif counter1 == 2: ##decrement counter (back to 1)
                counter1 -= 1
                start += datetime.timedelta(days=3) ##increment start date
            filepath = "images/" + file
            filestring = "<td>" + file + "</td>"
            startdate = start
            startstring = "<td>" + startdate.strftime("%B %d, %Y") + "</td>"
            enddate = startdate +datetime.timedelta(days=2) ##end date is two days later (for 3 day range)
            endstring = "<td>" + enddate.strftime("%B %d, %Y") + "</td>"
            daterange = startdate.strftime("%d%m%Y") + "-" + enddate.strftime("%d%m%Y")
            img = Image.open(filepath)
            crop = img.crop(cropdimensions)
            cropname = splitname[0] + "crop.jpg"
            croppath =  'crops/' + cropname
            crop.save(croppath)
            cropstring = "<td><img src=\"" + croppath + "\"></td>"
            rowstring= "<tr>" + filestring + startstring + endstring + cropstring + "</tr>"
            htmltablestring += rowstring
            newfile = ledger + spacer + reel + spacer + item + spacer + daterange + spacer + filepath
            rows.append([reel,  item,  file, newfile, startdate,  enddate,  ledger])

#Write each row in rows into a CSV file called results.csv
with open('results.csv',  'w',  newline='',  encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in rows:
        writer.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

#Combine the html strings into one and write it to a file called results.html
htmltablestring += "</table>"
htmlstring = htmlstart + htmltablestring + htmlend
htmlfile = open('results.html',  'w')
htmlfile.write(htmlstring)
htmlfile.close()
