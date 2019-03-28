
# Python Executable Definition
$Python = "python.exe"


# Python Script to execute
$Script     = "C:\PS\ProperNames.py"


$targetPath = "C:\PS\Text\*.txt"


$files = Get-ChildItem $targetPath


Write-Host "Multiple File Processor v 1.0"
Write-Host "Files to Process"
$files


foreach ($file in $files) 
{
Write-Host "Processing File: " $file
Get-Content $file -Raw | & $Python $Script
}


