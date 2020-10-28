"""
@author: Erwin Pannecoucke
"""

arguments_message = """
Usage:
    FK_cleaner.py [--debug] [--help]

       no arguments:     No output

       --debug:          Enable more verbose output
       --help:           Show some explanation about this program.

    """

help_message = """
While using the familiekiosk, I noticed over time that 
  [*] some photo's were downloaded incorrectly, and had a filesize of 0 mb. This caused FK_TVbox.py to crash, as PIL couldn't open the photo.
  [*] sometimes people uploaded "wrong" stuff (e.g. video's), which were downloaded as well ended up in the PICS folder.
  
This script checks for every file in the PICS folder if:
  1. The file is bigger than 0. If not, the file gets deleted.
  2. The file extension is allowed in that directory. 

To work correctly, this script should be run as a service in the background, just as FK_ChatBot.py and FK_TVbox.py

    """

def FK_cleaner(path, allowed_formats, remove = False, debug = False):

    def check_filesize(file, remove=False, debug = False):

        """
        Checks the filesize and returns True if oke, False if bad
        """

        size = os.path.getsize('{}'.format(file))
        if debug == True: print("\n   Filesize is {} bytes".format( size ))

        if remove == True and size == 0:
            os.remove(file)
            print("FK_cleaner: removed zero-file {} ".format(file))

        return()


    def check_format(file, allowed_formats, remove=False, debug = False):
        """
        Checks the file format and returns True if oke, False if bad
        """

        filename_extension = file.split(".")[-1]
        if filename_extension not in allowed_formats:
            if debug == True: print("\n   Wrong file format for: {}".format(file))
            if remove == True:
                os.remove(file)
                print("FK_cleaner: removed wrong file {}".format(file))




    for file in glob.glob(r'{}*.*'.format(path)): # For every file in that directory
        if debug == True: print("\nChecking file: {}".format(file))

        # Always check if a file is still there before performing any action.
        if os.path.isfile(file):
            check_filesize(file, remove=remove, debug = debug)

        if os.path.isfile(file):
            check_format(file, allowed_formats, remove=remove, debug = debug)


##############################################
#                                            #
#         ACTUAL START OF THE SCRIPT         #
#                                            #
##############################################

import os
import sys
import glob


if sys.version_info[0] != 3:
    print("\n   ERROR:\
           \n   You are using the following Python version: {}.\
           \n\n   This script is only compatible with Python3.\
           \n   Please restart the script with \"python3 score_images.py\".".format(sys.version))

    exit()

if "--debug" in sys.argv:
    print("\nDebugging enabled\n")
    debug = True
    sys.argv.remove("--debug")
else:
    debug = False

if len(sys.argv) > 2:
    print("Too many arguments!")
    print(arguments_message)
    exit()

elif len(sys.argv) - 1 == 0:  # No more arguments -> run this shit
    BASE_PIC_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/pics/'
    if debug == True: print("Start cleaning folder {} with debuging {}".format(BASE_PIC_PATH, debug))
    FK_cleaner(BASE_PIC_PATH, allowed_formats = ["jpg", "metafile"], remove = True, debug=debug)

elif sys.argv[1] == "--help":
    print(arguments_message)
    print(help_message)
    exit()


else:
    print("\nInvalid input!")
    print(arguments_message)
    exit()
