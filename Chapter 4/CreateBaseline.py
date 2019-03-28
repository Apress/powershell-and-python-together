''' 
Step One Create a baseline hash list of target folder
December 2018, Python Forensics

'''

''' LIBRARY IMPORT SECTION '''

import subprocess       # subprocess library
import argparse         # argument parsing library
import os               # Operating System Path
import pickle           # Python object serialization 

'''ARGUMENT PARSING SECTION '''

def ValidatePath(thePath):
    ''' Validate the Folder thePath
        it must exist and we must have rights
        to read from the folder.
        raise the appropriate error if either
        is not true
    '''
    # Validate the path exists
    if not os.path.exists(thePath):
        raise argparse.ArgumentTypeError('Path does not exist')

    # Validate the path is readable
    if os.access(thePath, os.R_OK):
        return thePath
    else:
        raise argparse.ArgumentTypeError('Path is not readable')

#End ValidatePath ===================================

''' Specify and Parse the command line, validate the arguments and return results'''

parser = argparse.ArgumentParser('File System Baseline Creator with PowerShell- Version 1.0 December 2018')
parser.add_argument('-b', '--baseline',   required=True, help="Specify the resulting baseline file")
parser.add_argument('-p', '--Path',       type= ValidatePath, required=True, help="Specify the target folder to baseline")
parser.add_argument('-t', '--tmp',        required=True, help="Specify a temporary result file for the PowerShell Script")

args = parser.parse_args()   

baselineFile = args.baseline
targetPath   = args.Path
tmpFile      = args.tmp

''' MAIN SCRIPT SECTION '''
if __name__ == '__main__':

    try:
        ''' POWERSHELL EXECUTION SECTION '''
        print()
        command = "powershell -ExecutionPolicy ByPass -File C:/PS/HashAcquire.ps1"+" -TargetFolder "+ targetPath+" -ResultFile "+ tmpFile 
        print(command)
        print()
        powerShellResult = subprocess.run(command, stdout=subprocess.PIPE)
        if powerShellResult.stderr == None:
        
            ''' DICTIONARY CREATION SECTION '''
            baseDict = {}
            
            with open(tmpFile, 'r') as inFile:
                for eachLine in inFile:
                    lineList = eachLine.split()
                    if len(lineList) == 2:
                        hashValue = lineList[0]
                        fileName  = lineList[1]
                        baseDict[hashValue] = fileName
                    else:
                        continue
        
            with open(baselineFile, 'wb') as outFile:
                pickle.dump(baseDict, outFile)
                print("Baseline: ", baselineFile, " Created with:", "{:,}".format(len(baseDict)), "Records")
                print("Script Terminated Successfully")
        else:
            print("PowerShell Error:", p.stderr)
            
    except Exception as err:
        print ("Cannot Create Output File: "+str(err))
        quit()
    
    
    
    
