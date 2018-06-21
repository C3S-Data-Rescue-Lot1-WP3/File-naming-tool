# !/usr/bin/python
# script written by VCS Apr 4 2016, to re-assign ledger types


#imagefolder = '1491_McGill_Observatory_Master/Ledger_type_C/'
#for file in sorted(os.listdir(imagefolder)): ##images are read in order
file_name_string= "1491_B_14_1881-01-01_1881-01-03_1.jpg"

new_ledger_type="C"
if file_name_string[5] != "C" :
 print (file_name_string[5])
 newfilename= file_name_string(str.replace(file_name_string[5],"C"))
 print(newfilename)
 
 
 
 
 