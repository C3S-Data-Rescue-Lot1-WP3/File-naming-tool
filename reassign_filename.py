# !/usr/bin/python
# script written by VCS Apr 4 2016, to re-assign ledger types 
# originally written in ruby, port to python
import os
import datetime
import csv
import shutil
newfolder="1491_test"
ledgerfolder="Ledger_G/"
#newfolder= "1491_McGill_Observatory_Master"
# open Item_reverse_test_check_name_results.csv
namesfile='Item109_Reel14_1935_check_name_results.csv'
# function to rename files and copy them the the master directory
def copy_rename(old_file_name, new_file_name, old_folder,new_folder):
        src_dir= old_folder 
        dst_dir= os.curdir + "/" + new_folder 
        src_file = old_file_name
        dst_file= new_file_name
        source= src_dir + "/" + src_file
        destination= dst_dir + "/" + dst_file
#        print(source,destination)
        shutil.copy(source,destination)
     
#Reel,Item,File,New file,Start date,End date,Ledger type
oldfilepath=[ledgerfolder]
oldfilename=[]
newfilename=[]
file_info=[]
imagefolder=' '
splitname = namesfile.split('_')
#print(splitname)
imagefolder = ledgerfolder + str(splitname[0]) + '_' + str(splitname[1]) +'_' + str(splitname[2]) +'_' +str(splitname[3])
print(imagefolder)
# read in old and new filenames from csv
counter1=0

with open(ledgerfolder+namesfile,'r',newline='') as csvfile:
       filereader = csv.reader(csvfile)
       for row in filereader:
         file_info = row
         if file_info[0] != 'Reel':
          oldfilepath.append(file_info[2])
          split_oldfile = file_info[2].split('/')
          oldfilename.append(split_oldfile[1])
          newfilename.append(file_info[3]+ '.jpg')
          print(oldfilepath[counter1],oldfilename[counter1],newfilename[counter1])
          counter1 += 1

counter2=0
for file in sorted(os.listdir(imagefolder)): ##images are read in order 
  print(counter2,file)
  copy_rename (oldfilename[counter2], newfilename[counter2], imagefolder, newfolder)
  print(counter2,oldfilename[counter2], newfilename[counter2], imagefolder, newfolder)
  counter2 += 1



 
 
 
 