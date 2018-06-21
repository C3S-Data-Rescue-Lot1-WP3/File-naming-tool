#!/usr/bin/env python


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
# need to switch page 1 and page 2 in csv files
reel = "1"
item = "1"
ledger = "A"
imagefolder = 'test/'
cropdimensions =(1300,  100,  2200,  250) # item 13
#cropdimensions =(2500,  200,  4000,  450)  # item 7
#cropdimensions = (1700,  220,  2900,  500)  # item 5 ##values are x.y for top left and x.y for bottom right of crop area (in that order)
start = datetime.date(1983, 7, 1)
spacer = "_" ##used in new file names
numpages = 2
daysperpage = 3
pagestepping = 1 ## Set to -1 if page decreases
lastday_offsetfrom_firstday = abs(daysperpage) -1
resultsname = imagefolder[:-1] #resultsname is the name to be appended to files to indicate which Item and folder they're from
print (resultsname)
resultsprefix = resultsname +'_' #resultsprefix to add to results files to indicate which folder it being checked



#prepare HTML output
htmlstart="<!DOCTYPE html><html><head><title>Results</title></head><body>"
htmltablestring="<table border=\"1\">"
htmltablestring += "<tr><td>File</td><td>Start date</td><td>End date</td><td>Image crop</td><td>thumbnail</td><td>Page #</td></tr>" ##html table 1st row (colum names)
htmlend="</body></html>"

#prepare CSV output ('rows' list)
rows = []
rows.append(["Reel",  "Item",  "File",  "New file",  "Start date", "End date",  "Ledger type"]) ##CSV 1st row (column names)

#cleanup the script's folder: delete any 'crops' folders, results.html and results.csv files
if (os.path.isdir(resultsprefix + 'crops') & os.path.exists(resultsprefix + 'crops')):
    shutil.rmtree(resultsprefix + 'crops')
    os.mkdir(resultsprefix + 'crops')
else:
    os.mkdir(resultsprefix + 'crops')
if os.path.exists(resultsprefix +'check_name_results.html'): #modified to include resultsprefix
    os.unlink(resultsprefix +'check_name_results.html')
if os.path.exists(resultsprefix +'check_name_results.csv'):
    os.unlink(resultsprefix +'check_name_results.csv')

#for each image in images folder: guess dates, save a crop from image, save info into rows[] and HTML table
if pagestepping < 0:
    counter1 = daysperpage + 1
else:
    counter1 = 0
for file in sorted(os.listdir(imagefolder)): ##images are read in order
    if '.' in file:
        splitname = file.rsplit('.', 1)
        if splitname[1] in ["jpg",  "JPG"]:
            thisrow = ""
            counter1 += pagestepping
            if counter1 > numpages:
                counter1 = 1
                start += datetime.timedelta(days=daysperpage) ##increment start date
            if counter1 == 0:
                counter1 = numpages
                start += datetime.timedelta(days=daysperpage) ##increment start date
            filepath = imagefolder + "/" + file ##filepath = os.path.normpath(imagefolder + "/" + file)
            filestring = "<td>" + file + "</td>"
            startdate = start
            startstring = "<td>" + startdate.strftime("%B %d, %Y") + "</td>"
            enddate = startdate +datetime.timedelta(days=lastday_offsetfrom_firstday) ##end date is 0-6 days later
            endstring = "<td>" + enddate.strftime("%B %d, %Y") + "</td>"
            daterange = startdate.strftime("%Y-%m-%d") + spacer + enddate.strftime("%Y-%m-%d")
            img = Image.open(filepath)
            crop = img.crop(cropdimensions)
            cropname = splitname[0] + "crop.jpg"
            croppath =  resultsprefix + 'crops/' + cropname
            crop.save(croppath)
            cropstring = "<td><img src=\"" + croppath + "\" WIDTH=600></td>"
            thumbstring = "<td><img src=\"" + filepath + "\" WIDTH=200></td>"
            pagenumstring = "<td>"+str(counter1)+"</td>"
            rowstring= "<tr>" + filestring + startstring + endstring + cropstring + thumbstring + pagenumstring+ "</tr>" + "\n"
            htmltablestring += rowstring
            newfile = '1491' + spacer + ledger + spacer + item + spacer + daterange + spacer + str(counter1)
            rows.append([reel,  item,  imagefolder+file, newfile, startdate,  enddate,  ledger])

#Write each row in rows into a CSV file called results.csv
with open(resultsprefix + 'check_name_results.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in rows:
        writer.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

#Combine the html strings into one and write it to a file called results.html
htmltablestring += "</table>"
htmlstring = htmlstart + htmltablestring + htmlend
htmlfile = open(resultsprefix + 'results.html',  'w')
htmlfile.write(htmlstring)
htmlfile.close()
