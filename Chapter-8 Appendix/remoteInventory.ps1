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
Specifies the computer to collect the USB Activity

.parameter UserName
Specifies the Administrator UserName on the Target Computer

.parameter outFile
Specifies the full path of the output file

.example

HashAcquire 
Collects the USB Activity on the target Computer
#>


# Parameter Definition Section
param(  
    [string[]]$targetComputer=$env:COMPUTERNAME,
    [string]$userName,
    [string]$targetFolder="c:/",
    [string]$ResultFile="c:/PS/inventory.txt"
)



Get-ChildItem $TargetFolder | Get-FileHash | Select-Object -Property Hash, Path | Format-Table -HideTableHeaders | Out-File $ResultFile -Encoding ascii

