''' 
Step Twp Verify a baseline hash list against a target folder
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

parser = argparse.ArgumentParser('File System Baseline Validation with PowerShell- Version 1.0 December 2018')
parser.add_argument('-b', '--baseline',   required=True, help="Specify the source baseline file to verify")
parser.add_argument('-p', '--Path',       type= ValidatePath, required=True, help="Specify the target folder to verify")
parser.add_argument('-t', '--tmp',        required=True, help="Specify a temporary result file for the PowerShell Script")

args = parser.parse_args()   

baselineFile = args.baseline
targetPath   = args.Path
tmpFile      = args.tmp

def TestDictEquality(d1,d2):
    """ return True if all keys and values are the same
        otherwise return False
    """
    if all(k in d2 and d1[k] == d2[k] for k in d1):
        if all(k in d1 and d1[k] == d2[k] for k in d2):
            return True
        else:
            return False
    else:
        return False
    
    '''
    return all(k in d2 and d1[k] == d2[k]
               for k in d1) \
        and all(k in d1 and d1[k] == d2[k]
               for k in d2)
    '''

def TestDictDiff(d1, d2):
    """ return the subset of d1 where the keys don't exist in d2 or
        the values in d2 are different, as a dict """
    
    diff = {}
    
    for k,v in d1.items():
        if k in d2 and v in d2[k]:
            continue
        else:
            diff[k+v] = "Baseline Missmatch"
            
    return diff

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
            # Load in the baseline dictionary
            
            with open(baselineFile, 'rb') as baseIn:
                baseDict = pickle.load(baseIn)
            
            # Create a new dictionary for the target folder
            newDict  = {}
            
            with open(tmpFile, 'r') as inFile:
                for eachLine in inFile:
                    lineList = eachLine.split()
                    if len(lineList) == 2:
                        hashValue = lineList[0]
                        fileName  = lineList[1]
                        newDict[hashValue] = fileName
                    else:
                        continue
                    
            ''' DICTIONARY TEST SECTION '''
            if TestDictEquality(baseDict, newDict):
                print("No Changes Detected")
            else:
                diff = TestDictDiff(newDict, baseDict)
                print(diff)
                        
        else:
            print("PowerShell Error:", p.stderr)
            
    except Exception as err:
        print ("Cannot Create Output File: "+str(err))
        quit()
    
    
    
    
