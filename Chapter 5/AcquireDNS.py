''' 
Acquire DNS Scripts from a Remote Computer
Version 1.0 January 2018 
Author: Chet Hosmer

'''

''' LIBRARY IMPORT SECTION '''

import subprocess       # subprocess library
import argparse         # argument parsing library
import os               # Operating System Path

'''ARGUMENT PARSING SECTION '''

def ValidateFile(theFile):
    ''' Validate the File exists
        it must exist and we must have rights
        to read from the folder.
        raise the appropriate error if either
        is not true
    '''
    # Validate the file exists
    if not os.path.exists(theFile):
        raise argparse.ArgumentTypeError('File does not exist')

    # Validate the file is readable
    if os.access(theFile, os.R_OK):
        return theFile
    else:
        raise argparse.ArgumentTypeError('File is not readable')

#End ValidateFile ===================================

''' Specify and Parse the command line, validate the arguments and return results'''

parser = argparse.ArgumentParser('Remote Client DNS Cache with PowerShell- Version 1.0 January 2018')
parser.add_argument('-c', '--computer',  required=True, help="Specify a target Computer for Aquistion")
parser.add_argument('-u', '--user',      required=True, help="Specify the remote user account")
parser.add_argument('-t', '--tmp',       required=True, help="Specify a temporary result file for the PowerShell Script")
parser.add_argument('-s', '--srch',      required=True, type=ValidateFile, help="Specify the keyword search file")

args = parser.parse_args()   

computer = args.computer
user     = args.user
tmp      = args.tmp
srch     = args.srch

print("DNS Cache Acquisition\n")

print("Target:       ", computer)
print("User:         ", user)
print("Keyword File: ", srch)

'''KEYWORD LOADING SECTION '''

print("Processing Keyword Input")
try:
    with open(srch, 'r') as keywordFile:
        words = keywordFile.read()
        word = words.lower()
        words = words.strip()
        wordList = words.split()
        wordSet = set(wordList)
        keyWordList = list(wordSet)
        print("\nKeywords to search")
        for eachKeyword in keyWordList:
            print(eachKeyword)
        print()
except Exception as err:
    print("Error Processing Keyword File: ", str(err))
    quit()
    

''' MAIN SCRIPT SECTION '''
if __name__ == '__main__':

    try:
        ''' POWERSHELL EXECUTION SECTION '''
        print()
        command = "powershell -ExecutionPolicy ByPass -File C:/PS/CacheAcquire.ps1"+" -targetComputer "+ computer+ " -user "+user+ " -resultFile "+tmp 
        print("Executing: ", command)
        print()
        
        powerShellResult = subprocess.run(command, stdout=subprocess.PIPE)
        
        if powerShellResult.stderr == None:
            
            '''DNS CACHE SEARCHING SECTION '''
            
            hitList = []
            try:
                with open(tmp, 'r') as results:
                    for eachLine in results:
                        eachLine = eachLine.strip()
                        eachLine = eachLine.lower()
                        for eachKeyword in keyWordList:
                            if eachKeyword in eachLine:
                                hitList.append(eachLine)
            except Exception as err:
                print("Error Processing Result File: ", str(err))
                
            '''RESULT OUTPUT SECTION '''
            
            print("Suspicous DNS Cache Entries Found")
            for eachEntry in hitList:
                print(eachEntry)

            print("\nScript Complete")
        else:
            print("PowerShell Error:", p.stderr)
            
    except Exception as err:
        print ("Cannot Create Output File: "+str(err))
        quit()
    
    
    
    
