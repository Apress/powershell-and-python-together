
# Python Executable Definition
$Python = "C:\Python27\python.exe"

# Python Scrip that I wish to execute
$Script = "C:\PS\ProperNames.py"

# Obtain contents of file to extract
$rawContent = Get-Content C:\PS\Text\Dialog.txt -Raw 

# Pipe the output of the file content to the Python Script
$rawContent | & "C:\Python27\python.exe" "C:\PS\ProperNames.py"

