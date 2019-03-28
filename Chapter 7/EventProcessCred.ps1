
$targetComputer = "XXXXX"
$userName       = "XXXXX\YYYYY"


$password       = "ZZZZZZ"


$securePassword = ConvertTo-SecureString -AsPlainText $password -Force
$credential     = New-Object System.Management.Automation.PSCredential -ArgumentList $userName, $securePassword

Invoke-Command -ComputerName $targetComputer -Credential $credential -ScriptBlock {Get-Eventlog -LogName system -Newest 100}