#
# Simple file Inventory Script
#

# Function to convert size values to human readable 
function GetMBSize($num) 
{
    $suffix = "MB"
    $MB = 1048576

    $num = $num / $MB

    "{0:N2} {1}" -f $num, $suffix
}

# Set Report Title
$rptTitle = "File Inventory"
# Get the current date and tme
$rptDate=Get-Date

# Set the target Directory and parameters
$targetDirectory = "c:\"

# Create HTML Header Section
$Header = @"
<style>
TABLE {border-width: 1px; border-style: solid; border-color: black; border-collapse: collapse;}
TD {border-width: 1px; padding: 3px; border-style: solid; border-color: black;}
</style>
<p>
<b> $rptTitle</b>
<p>
<b> Date: $rptDate </b>
<p>
<b> Target: $targetDirectory </b>
<p>
"@

# Provide script output for user
Write-Host "Create Simple File Inventory"

$dir = Get-ChildItem $targetDirectory -File -Hidden

# Create an empty array to hold values
$outArray = @()

# Loop through each file found
foreach ($item in $dir)
{
    # create and object to hold item values from separate CmdLets
    $tempObj = "" | Select "FileName", "Attribute", "Size", "HashValue"

    # Get the fullname including path
    $fullName  = $item.FullName

    # Get the attributes assoicated with this file
    $attributes = $item.Attributes
    $size       = GetMBSize($item.Length)

    # Generate the SHA-256 Hash of the file
    $hashObj = Get-FileHash $fullName -ErrorAction SilentlyContinue
    # Get just the Hash Value
    $hashValue = $hashObj.Hash

    # if hash value could not be generated set to Not Available
    if ([string]::IsNullOrEmpty($hashValue))
    {
        $hashValue = "Not Available"
    }

    # Fill in the tempObj 
    $tempObj.FileName  = $fullName
    $tempObj.Attribute = $attributes
    $tempObj.Size      = $size
    $tempObj.HashValue = $hashValue

    # Add the tempObj to the outArray
    $outArray += $tempObj

    # Clear the output array
    $tempObj = $null
}

$outArray | ConvertTo-Html -Head $Header -Property FileName, Attribute, Size, HashValue |
 Out-File test.html

#$outArray | ConvertTo-Html | out-file test.html
Write-Host "Script Completed"
Write-Host "test.html created"






