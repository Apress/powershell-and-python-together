'''
BasicOnev3.py
Script to display string 
passed to script from PowerShell
'''

# import standard module sys
import sys

print("Welcome to Python\n")
print("Data Received from PowerShell\n")

for eachLine in sys.stdin:
    print(eachLine)
    
