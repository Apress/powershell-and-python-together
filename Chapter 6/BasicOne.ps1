
# Python Executable Definition
$Python = "C:\Python27\python.exe"


# Python Scrip that I wish to execute
$Script = "C:\PS\BasicOne.py"


Write-Host "Pass a String to Python"
$Message = "Hello Python - Hello Universe"


Write-Host
$Message | & $Python $Script



