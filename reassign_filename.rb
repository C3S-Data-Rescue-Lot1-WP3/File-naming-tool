# !/usr/bin/ruby
# script written by VCS Apr 4 2016, to re-assign ledger types
require 'fileutils'
# open Item_reverse_test_check_name_results.csv

#Reel,Item,File,New file,Start date,End date,Ledger type
oldfilepath=Array.new
newfilename=Array.new
counter1=0
csv_file='Item_reverse_test_check.csv'
File.foreach(csv_file) do |row|
 next if row.include? "Reel"  # skip first line with header information
 counter1 += 1
 file_info=row.split(',')
 oldfilepath[counter1]=file_info[2]
 newfilename[counter1]=file_info[3]+ '.jpg'
end
	 
# construct name of folder to open for renaming from csv_file name
foldername= csv_file.split('_')                                                                                                                                                                                                                                                                                                                      
imagefolder =foldername[0]+'_' + foldername[1] + '_' +foldername[2]

counter2=0
Dir.foreach (imagefolder) do |filename|
 next if filename == '.' or filename == '..'
 counter2 += 1
# puts filename, oldfilepath[counter2].to_s,imagefolder.to_s + '/' + newfilename[counter2].to_s
 FileUtils.cp(oldfilepath[counter2].to_s, imagefolder.to_s + '/' + newfilename[counter2].to_s)  
end


 
 
 
 