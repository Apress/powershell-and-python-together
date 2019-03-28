<#
.synopsis
Collect ClientDnsCache

- User Specifies the target computer 

The script will produce a simple ascii output file containing
the recent DnsCache from the target computer

.Description
This script collects DnsCache from the Target Computer

.parameter targetComputer
Specifies the computer to collect the USB Activity

.parameter user
Specifies the Administrator UserName on the Target Computer

.parameter resultFile
Specifies the full path of the output file

.example

CacheAcquire 
Collects the recent DnsCache from the target computer
#>


# Parameter Definition Section
param(  
    [string]$user,
    [string]$targetComputer,
    [string]$resultFile
)

# Obtain the ClientDnsCache from target computer and store the result in a local variable
$r = Invoke-Command -ComputerName $targetComputer -Credential $user -ScriptBlock {Get-DnsClientCache | Select-Object -Property Entry | Out-String}

# Write the resulting list in simple ascii to a specified local file
$r
$r | Out-File $resultFile -Encoding ascii



