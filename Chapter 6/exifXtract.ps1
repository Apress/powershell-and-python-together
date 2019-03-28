
# Python Executable Definition
$Python = "python.exe"


# Python Scrip that I wish to execute
$Script = "C:\PS\pyExif.py"


$files = Get-ChildItem C:\PS\Photos\*.jpg 
$jpegList = $files | Select-Object FullName | Format-Table -HideTableHeaders


$jpegList | & $Python $Script
