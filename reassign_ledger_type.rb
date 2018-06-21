# !/usr/bin/ruby
# script written by VCS Apr 4 2016, to re-assign ledger types

imagefolder = '1491_McGill_Observatory_Master/Ledger_type_G/'
Dir.foreach (imagefolder) do |filename|
 next if filename == '.' or filename == '..'
 puts filename
 file_name_string= filename
 if file_name_string[0] == "1"
  if file_name_string.include? '_' 
  puts file_name_string[5]
   newfilename= file_name_string.gsub('_G_','_Ga_')
   puts filename, newfilename
   File.rename(imagefolder + filename,imagefolder + newfilename)  
  end
 end 
end 
 
 
 
 
 