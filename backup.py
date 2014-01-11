#!/usr/bin/python
import os, time, sys, shutil, distutils.core, zipfile
from datetime import datetime

def main():
   try:
      with open("log.txt") as file:
         Read_file()
   except IOError:
      #if the program has never been run before, there will be no log.txt
      #which means we have to configure the program
      Configuration()



'''
This function appends the date of the backup being done to our log.txt
which is needed to see if a backup should be run or not when the program
is executed
'''
def Update_log(cur_date):
   try:
      f = open("log.txt", 'a')
      f.write(cur_date + "\n")
   except IOError:
      print "No log.txt, welp, that's not good. Exiting..."
      exit()
   else:
      f.close()
      print "log.txt was updated and closed"



'''
This function deletes the non-zip folders
'''
def Delete_dir(dir):
   shutil.rmtree(dir)



'''
This function zips our destination directories up and then makes sure that
the zip is made so it can call the Delete_dir() function
'''
def Zip_dir(dir):
   zip = zipfile.ZipFile(dir+'.zip', 'w')
   for root, dirs, files in os.walk(dir):
      for file in files:
         zip.write(os.path.join(root, file))
   
   if os.path.exists(dir+'.zip'):
      Delete_dir(dir)
   print "done"



'''
This function is only run if log.txt is not found. It sets up the config.txt
file by asking for the sources, destinations, and how often the user wants
to back up their data. It also makes the config.txt file
'''
def Configuration():
   source_l = []
   dest_l   = []
   
   print("Hello, it appears you haven't run this program before, let me ask \
you a few questions so this doesn't happen again")

   num_sources = raw_input("How many sources do you want to backup?")
   for sources in xrange(0, int(num_sources)):
      source = raw_input("Enter your source: ")
      source_l.append(source)

   num_dests = raw_input("How many destinations do you want to backup?")
   for dests in xrange(0, int(num_dests)):
      dest = raw_input("Enter your destination: ")
      dest_l.append(dest)

   freq = raw_input("How often would you like to backup? (hours, days, etc)")

   #creates the config file
   f = open('backup_config.txt', 'w')

   #data is grouped by type, either frequency, source, or destination, this
   #is denoted by the 'FREQ ', 'SOURCE ', 'DEST ' written in front of them
   #to make it easier to read in the data later on
   f.write("FREQ %s\n" %(freq))
   
   for i in xrange(0, len(source_l)): 
     f.write("SOURCE %s\n" %(source_l[i]))
   for i in xrange(0, len(dest_l)):
      f.write("DEST %s\n" %(dest_l[i]))
      
   f.close()


 
'''
This function checks to see how long it's been since our last backup, and if
we should run another one by checking the frequency in the config.txt
'''
def analyze_freq(freq):
   cur_date = time.strftime("%H-%d-%m-%Y")
   interval = freq[2:] #parses for the chars to the right of the 2nd
   freq = freq[:1] #parses for the 1st char on the left

   try:
      f = open('log.txt', 'r')

      #this line gets the last line in our log.txt
      last_run = (list(f)[-1])
   except IOError:
      print "Couldn't open log.txt, that isn't good, exiting..."
      exit()
   else:
      f.close()

   #all of these check to see what time interval the user specified
   #i.e. hour, day, month, and then compares it against the current date
   if interval == "hour" or interval == "hours":
      #b/c the date is stored hour-day-month-year, hour is the 1st two chars
      delta = int(cur_date[:2]) - int(freq)

      if delta >= int(last_run[:2]):
         print "it's been an hour, run the backup!"
         return
      else:
         print "Not yet, exiting..."
         exit()
         
   elif interval == "day" or interval == "days":
      delta = int(cur_date[3:5]) - int(freq)

      if delta >= int(last_run[3:5]):
         print "it's been a day, run the backup!"
         return
      else:
         print "not yet, exiting..."
         exit()
   
   elif interval == "week" or interval == "weeks":
      delta = int(cur_date[6:8]) - int(freq)
      
      if delta >= int(last_run[6:8]):
         print "it's been a week, run the backup!"
         return
      else:
         print "Not yet, exiting..."
         exit()

   elif interval == "month" or interval == "months":
      delta = int(cur_date[9:11]) - int(freq)
      
      if delta >= int(last_run[9:11]):
         print "it's been a month, run the backup!"
         return
      else:
         print "not yet, exiting..."
         exit()



'''
This function reads in our frequecy, sources, and destinations from our
config.txt and loads the arrays, and sends the frequency off to
analyze_freq() to see if we should run the backup. Also calls Create_backup()
'''      
def Read_file():
   source_l = []
   dest_l   = []
   
   if(os.path.isfile('backup_config.txt')):
      f = open('backup_config.txt', 'r')

      for line in f:
         if(line[:5] == "FREQ "):
            #You only want to send the frequency, not the "FREQ "
            analyze_freq(line[5:].strip("\n"))

         if(line[:7] == "SOURCE "):
            #this adds the source dir to our list without "SOURCE "
            source_l.append(line[8:])

         if(line[:5] == "DEST "):
            dest_l.append(line[6:])

      #this can be called here b/c if it wasn't time to run a backup
      #analyze_freq() would have exited the program for us
      Create_backup(source_l, dest_l)
   else:
      print("Config file not found, you shouldn't be seeing this...")
      exit()



'''
This function actually creates the backup, it walks through our destinations
and for each one it adds each source. It creates the backup file by using
the current date in the format hour-day-month-year. Also calls Update_log()
'''
def Create_backup(source_l, dest_l):
   cur_date = time.strftime("%H-%d-%m-%Y")

   for dests in xrange(0, len(dest_l)):
      #this creates our folder with the current date
      #strip is like chomp() from Perl but you can specify what whitespace
      dir_name = os.path.join(dest_l[dests].strip("\n"), cur_date)
     
      for sources in xrange(0, len(source_l)):
         src = source_l[sources].strip("\n")
         try:
            #distutils copy_tree() works better than shutils copy_tree()
            #b/c it doesn't have to create the destination if it's already
            #there unlike shutils.
            distutils.dir_util.copy_tree(src, dir_name)
         except DistutilsFileError:
            print "Src was not a dir, exiting..."
            exit()
      Zip_dir(dir_name)

   Update_log(cur_date)

   

if __name__ == '__main__':
   main()



