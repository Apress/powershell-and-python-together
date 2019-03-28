<#
.synopsis
Collect Hash and Filenames from specified folder

- User Specifies the target computer 
- User Specifies the target folder

The script will produce a simple ascii output file containing 
SHA-256Hash and FilePath

.Description
This script collects Hash and Filenames from specified computer and folder

.parameter targetComputer
Specifies the computer to collect the File Hash information

.parameter UserName
Specifies the Administrator UserName on the Target Computer

.parameter outFile
Specifies the full path of the output file

.example

HashAcquire 
Collects the File Hashes on the target Computer
#>


# Parameter Definition Section
param(  
    [string]$TargetFolder="c:/windows/system32/drivers/",
    [string]$ResultFile="c:/PS/baseline.txt"
)


Get-ChildItem $TargetFolder | Get-FileHash | Select-Object -Property Hash, Path | Format-Table -HideTableHeaders | Out-File $ResultFile -Encoding ascii

