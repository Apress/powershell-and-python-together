<#
.synopsis
Collect USB Activity from target computer

- User Specifies the target computer 

The script will produce an HTML output file containing details of USB Activity
on the specified target computer

.Description
This script collects USB Activity and target computers

.parameter targetComputer
Specifies the computer to collect the USB Activity

.parameter UserName
Specifies the Administrator UserName on the Target Computer

.example

USBAcquire ComputerName
Collects the USB Activity on the target Computer
#>

# Parameter Definition Section
param(  
    [string]$User,
    [string]$targetComputer
)

Invoke-Command -ComputerName $targetComputer -Credential $User -ScriptBlock {Get-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Enum\USBSTOR\*\* | Select FriendlyName} 