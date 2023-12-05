import ftplib
import os
import shutil
import re
import datetime
import schedule
import time


# Create a function to log the transfers
def log_transfer_file(name, loc, status):
    
    # Change directory to save the log
    os.chdir("../")
    
    # Get date, time
    now = datetime.datetime.now()
    
    # Type the text that needs to be logged
    log_line = f"On {now} the file named {name} transfer {loc} {status}\n"
    
    # Append the line to the log
    with open("file_transfer_log.txt", "a") as log_txt:
        log_txt.write(log_line)
    log_txt.close()
    
    # Go back to initial directory to continue execution
    os.chdir("files")

    
    
# This function transfer the files from a public FTP server
# to a folder named files in our directory
    
def transfer_from_FTP():


    # Put the information of a public FTP
    # The downloads depend on the files in the FTP server
    FTP_HOST = "ftp.dlptest.com"
    FTP_USER = "dlpuser"
    FTP_PASS = "rNrKYTX9g7z3RgJRmxWuGHbeu"

    # Access the FTP server and get the file names
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    folders = ftp.nlst()



    # start iterating through files
    for i, file in enumerate(folders):

        try:
            # Get the extension and files names with regex
            extension = re.search("([a-zA-Z0-9]+)(\.[a-zA-Z0-9]+)",file).group(2)
            file_name = re.search("([a-zA-Z0-9]+)(\.[a-zA-Z0-9]+)",file).group(1)
            filename_new = f"file{i+1}_{file_name}{extension}"
            filename = file

            # Discard extension that are .com or .exe
            if extension == ".com" or extension == ".exe":
                # Log the transfer
                log_transfer_file(filename,"from FTP to local directory", "failed for wrong extension.")
                

             
            else:
                # create the file names
                retr_str = "RETR " + file

                # retreibe the files from the FTP server
                with open(filename, "wb") as t_file:
                    ftp.retrbinary(retr_str, t_file.write)
                log_transfer_file(filename,"from FTP to local directory", "succeded.")
                
                # Change the name of the file
                os.rename(filename, filename_new)

        except:
            # Log the transfer
            log_transfer_file(filename,"from FTP to local directory", "failed.")
            



# This function moves the files from 
# the files to another file using shutil
            
def transfer_to_internal_network():

    # set a destination folder
    dest = "../destination_folder"

    # Get the list of files that were downloaded
    files_fromFTP = os.listdir()

    # move files 1 by 1
    for file_move in files_fromFTP:

        # Use try not to overwrite the existing files with the same name
        try:
            shutil.move(file_move, dest)
            # Log the transfer success
            log_transfer_file(file_move,"from local directory to internal network", "succeded.")
        except:
            # Log the transfer failure
            log_transfer_file(file_move,"from local directory to internal network", "failed.")

            
# This function executes the whole transfer process    
    
def make_transfer():
    
    # Change directory to the destination of the files
    os.chdir("files")
    
    
    transfer_from_FTP()
    transfer_to_internal_network()
    
    # Return to initial directory
    os.chdir("../")
    
    
make_transfer()

# Scheduled the transfer every day at 12:00
schedule.every().day.at("12:00").do(make_transfer)


# Loop so that the scheduling task
# keeps on running all time.
while True:
 
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(2)
