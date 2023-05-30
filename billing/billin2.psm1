Param(
    [int] $monthDelta = -1
)
$ErrorActionPreference = "Stop"

Function Install-PowerShellModule {
    param (
        [Parameter(Mandatory=$true)]
        [String] $Name
    )
    # Installs required PowerShell modules
    Set-PSRepository -Name PSGallery -InstallationPolicy Trusted

    If (Get-Module -ListAvailable -Name $Name) {
        Write-Output "  Module $Name is available."
    } Else {
        Write-Output "  Module $Name is missing and will be installed."
        Install-Module -Name $Name -Force
    }

    Import-Module -Name $Name -Force

    <#
    .SYNOPSIS
    Installs and Imports the specified PowerShell Module

    .DESCRIPTION
    If the specified PowerShell Module isn't installed yet, it is installed.
    Nevertheless, the Module is reimported to the current session using Import-Module -Force.

    .INPUTS
    None. You cannot pipe objects to this cmdlet.

    .PARAMETER Name
    Name of the PowerShell Module

    .EXAMPLE
    PS> Install-Module -Name Az
    Ensures the Installation of the Azure Az PowerShell Modules

    .LINK

   #>
}

Function Install-Certificate {
    param (
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
        $Certificate,

        [Parameter(Mandatory=$false)]
        [String]$CertStoreLocation = "cert:\localmachine\my"
    )
    $existingLocalCert = Get-ChildItem -Path $CertStoreLocation | Where-Object {$_.ThumbPrint -eq $Certificate.Thumbprint}
    if ($null -eq $existingLocalCert)
    {
        Write-Output ("Installing Certificate with Thumbprint '{0}'" -f $Certificate.Thumbprint)
        $tempFile = New-TemporaryFile
        try {
            # Generate the password used for this certificate
            $null = Add-Type -AssemblyName System.Web -ErrorAction SilentlyContinue
            $certPwd = ConvertTo-SecureString -String ([System.Web.Security.Membership]::GeneratePassword(25, 10)) -AsPlainText -Force
            Export-PfxCertificate -Cert $Certificate -FilePath $tempFile.FullName -Force -Password $certPwd
            Import-PfxCertificate -FilePath $tempFile.FullName -CertStoreLocation $CertStoreLocation -Password $certPwd
        } finally {
            $tempFile.Delete()
        }
    } else {
        Write-Output ("Certificate with Thumbprint '{0}' already installed" -f $Certificate.Thumbprint)
        $existingLocalCert
    }

    <#
    .SYNOPSIS
    Installs the Certificate including Private Key in the specified location, if not yet present

    .DESCRIPTION
    Installs the Certificate including Private Key in the specified location, if not yet present

    .INPUTS
    Certificate to be installed

    .PARAMETER Certificate
    Certificate to be installed, must be exportable in order to get and install the private key as well

    .PARAMETER CertStoreLocation
    Location, where the Certificate is installed

    .EXAMPLE
    PS> Get-AutomationCertificate -Name 'AzureRunAsCertificate' | Install-Certificate
    Installs the AzureRunAsCertificate

    .LINK

  #>
}

# Main method
# Login to Azure - Testing if script is running in AzureAutomation
# Skip time consuming Az module install, as currently up-to-date
# Install-PowerShellModule -Name "Az"
If($PSPrivateMetadata.JobId) {
    Write-Output "Script is running in Azure-Automation ..."

    # install certificate
    Get-AutomationCertificate -Name 'AzureRunAsCertificate' | Install-Certificate

    # Get the connection "AzureRunAsConnection "
    $servicePrincipalConnection=Get-AutomationConnection -Name 'AzureRunAsConnection'

    Write-Output "Logging in to Az..."
    Login-AzAccount `
        -ServicePrincipal `
        -TenantId $servicePrincipalConnection.TenantId `
        -ApplicationId $servicePrincipalConnection.ApplicationId `
        -CertificateThumbprint $servicePrincipalConnection.CertificateThumbprint
} Else {
    Write-Output "Script is not running in Azure-Automation ..."
}

# -------------------------------------------------------
# CHANGE TO CORRECT SUBSCRIPTION
# -------------------------------------------------------
$subscriptionName = (Get-AzSubscription -SubscriptionId $servicePrincipalConnection.SubscriptionId).Name
Set-AzContext -SubscriptionId $servicePrincipalConnection.SubscriptionId
Get-AzContext

# -------------------------------------------------------
# CALCULATE THE DATE FROM RUN-DATE
# -------------------------------------------------------

[string]$Month = ((get-date).AddMonths($monthDelta)).ToString("yyyyMM")
$my = ([regex]"(?<y>\d{4})(?<m>\d{1,2})").Matches($Month)
$year_todelete = $my[0].Groups["y"].value
$month_todelete = $my[0].Groups["m"].value

$timeout = 10800 # 60 minutes - as delete may take a while

# -------------------------------------------------------
# USE THIS CONNETION STRING TO DATABASE
# -------------------------------------------------------

$kv = Get-AzKeyVault | Where-Object VaultName -like 'xto-coe-eu-commons*'
$Database = "billingdbnewtest"
$UserID = "buconfigadmin"

$PasswordSecret = (Get-AzKeyVaultSecret `
        -ResourceId $kv.ResourceId `
        -Name "buconfigdb-$UserID" `
        -ErrorAction Stop)
$Password = [System.Net.NetworkCredential]::new("", $PasswordSecret.secretValue).Password

$ServerSecret = (Get-AzKeyVaultSecret `
        -ResourceId $kv.ResourceId `
        -Name "buconfigdb-server" `
        -ErrorAction Stop)
$Server = [System.Net.NetworkCredential]::new("", $ServerSecret.secretValue).Password

$Server

$accesskeySecret = (Get-AzKeyVaultSecret `
        -ResourceId $kv.ResourceId `
        -Name "eabilling-token" `
        -ErrorAction Stop)
$accesskey = [System.Net.NetworkCredential]::new("", $accesskeySecret.secretValue).Password

$enrollmentNoSecret = (Get-AzKeyVaultSecret `
        -ResourceId $kv.ResourceId `
        -Name "eabilling-enrollmentno" `
        -ErrorAction Stop)
$enrollmentNo = [System.Net.NetworkCredential]::new("", $enrollmentNoSecret.secretValue).Password


$ConnectionString = "Data Source=$Server;Initial Catalog=$Database;Integrated Security=False;User Id=$userId;Password=$password;Connection Timeout=$timeout"



# -------------------------------------------------------
# USE THIS FOR CSV DOWNLOAD FROM EA PORTAL
# -------------------------------------------------------

$authHeaders = @{"authorization" = "bearer $accesskey"; "api-version" = "1.0"}
cd "C:\BillingDetails"
$csvPath = ".\Azure-Billing.csv"
$url = "https://consumption.azure.com/v3/enrollments/{0}/usagedetails/submit?billingPeriod={1}" -f $enrollmentNo, $Month


# -------------------------------------------------------
# DELETE DATA FROM TABLE IN TIMEFRAME
# -------------------------------------------------------

Write-Output "Connecting to SQL Server"
$sqlConnection = new-object System.Data.SqlClient.SqlConnection($connectionString)
$sqlConnection.open()

Write-Output "Deleting old data for: $year_todelete $month_todelete!"
$sqlDeleteCommand = $sqlConnection.CreateCommand()
$sqlDeleteCommand.CommandText = "DELETE FROM dbo.BillingDetails2 WHERE YEAR = {0} AND MONTH = {1} " -f $year_todelete, $month_todelete
$sqlDeleteCommand.CommandTimeout = $timeout
$sqlDeleteCommand.ExecuteNonQuery()


# -------------------------------------------------------
# DOWNLOAD CSV FROM EA PORTAL
# -------------------------------------------------------

Write-Output "Gathering billing Reports for Month: $month ..."

$webreq = Invoke-WebRequest $url -Headers $authHeaders -UseBasicParsing -Method Post
$content = $webreq.Content | ConvertFrom-Json
$ReportUrl = $content.reportUrl
do{
$reportreq = Invoke-WebRequest $ReportUrl -Headers $authHeaders -UseBasicParsing
sleep -Seconds 45
$reportreqcontent = $reportreq.Content | ConvertFrom-Json
$reportreqcontent
$Status = $reportreqcontent.status
If($Status -gt 3){
	throw "The report cannot be generated for this user and hence exit"
}

 } until ($Status -eq 3)
$blobpath = $reportreqcontent.blobPath
$id = $reportreqcontent.id
$pathid = '.\'+ $id
cd "C:\azcopy_windows_amd64_10.13.0"
.\azcopy.exe copy $blobpath "C:\BillingDetails"
cd "C:\BillingDetails"
$pathtoIDfile = "C:\BillingDetails\" + $id # where we copied the downloaded file

$filelist = @()
$filelist += $pathtoIDfile

# -------------------------------------------------------
# USE THIS FOR CSV DOWNLOAD FROM EA PORTAL, AMORTIZED
# -------------------------------------------------------
#
function Get-AccessToken {
   $context = Get-AzContext
   $profile = [Microsoft.Azure.Commands.Common.Authentication.Abstractions.AzureRmProfileProvider]::Instance.Profile
   $profileClient = New-Object -TypeName Microsoft.Azure.Commands.ResourceManager.Common.RMProfileClient -ArgumentList ($profile)
   $token = $profileClient.AcquireAccessToken($context.Subscription.TenantId)
   return $token.AccessToken
}

$rm_endpoint = "https://management.azure.com"
$authHeader = @{
'Content-Type'  = 'application/json'
'Authorization' = 'Bearer ' + (Get-AccessToken)
}

# setting amortized CSV name to a pattern that will be picked up with the normal billing splits
$counter = 0
$urlAmortized = 'https://management.azure.com/providers/Microsoft.Management/managementGroups/eXtollo_production/providers/Microsoft.CostManagement/query?api-version=2019-11-01'
$ReservationIDs = @(
    '"5333f279-be6e-4c98-ab83-1c593f2e9b77"',  #Central_Reservation35_VM_RI_12-08-2022
    '"de60024d-7de2-47f4-86a7-630f3d350e5a"',  #Central_Reservation34_VM_RI_12-08-2022
    '"7e460da4-269a-4095-8d99-9ccce49c92d1"',  #Central_Reservation33_VM_RI_12-08-2022
    '"85b4c2c6-9881-4e16-a2fd-bdd8fd5f7cbb"',  #Central_Reservation32_VM_RI_12-08-2022
    '"a9bf842e-4381-4ddd-9930-91793c0cdf08"',  #Central_Reservation31_VM_RI_12-08-2022
    '"8a5129ac-bcec-4658-8f18-6b2dfaf3eed7"',  #Central_Reservation30_VM_RI_12-08-2022
    '"456a5f36-0395-4c4e-ac37-032f6461f0c6"',  #Central_Reservation29_VM_RI_12-08-2022_17-23
    '"54cd599b-8118-476e-b992-daa42846e7a6"',  #Central_Reservation28_VM_RI_12-08-2022
    '"6a4a903f-93f3-42d2-88c8-f9e2c03e83d8"',  #Central_Reservation27_VM_RI_12-08-2022
    '"dcdf5846-daec-4dc4-93d1-9f31342ae708"',  #Central_Reservation26_VM_RI_12-08-2022
    '"4e78218e-08f6-418b-b6e0-0de29de5e331"',  #Central_Reservation25_VM_RI_12-08-2022
    '"b513f3ae-6371-407b-bd19-d59c27bd165b"',  #Central_Reservation24_VM_RI_12-08-2022
    '"ad4d68d0-81d5-4142-91e9-beffdb989686"',  #Central_Reservation23_VM_RI_12-08-2022
    '"62327547-a938-4773-8019-d5084998068f"',  #Central_Reservation22_VM_RI_12-08-2022
    '"6145d9c3-c04a-41f9-b917-05eb59dc343d"',  #Central_Reservation21_VM_RI_12-08-2022
    '"6ed9f977-1145-4f84-9d05-0324a3406edc"',  #Central_Reservation20_VM_RI_12-08-2022
    '"4cc01eae-d718-44af-8854-ed99c11e681e"',  #Central_Reservation4_Postgresql_RI_31-05-2022
    '"f56a900a-dbd8-42fb-9786-2328edec963d"',  #Central_Reservation1_Postgresql_RI_31-05-2022
    '"c67a572d-d803-4c7f-808d-f11ba766b064"',  #Central_Reservation2_Postgresql_RI_31-05-2022
    '"1120ed93-f8b8-46cf-9869-c8ed63573dba"',  #Central_Reservation5_Postgresql_RI_31-05-2022
    '"9c238aee-360c-4c1b-8960-0a9feb675233"',  #Central_Reservation3_Postgresql_RI_31-05-2022
    '"969cde79-99aa-4262-aa39-df00f244387b"',  #Central_Reservation2_2_SQLDB_RI_31-05-2022
    '"d634b0c2-c6f6-4f36-9e26-10e1e38727f2"',  #Central_Reservation4_2_SQLDB_RI_31-05-2022
    '"cba4d6cb-94ed-4bc2-9394-d93f84e6cf9d"',  #Central_Reservation3_2_SQLDB_RI_31-05-2022
    '"123c1a87-5fc8-4f24-844a-5b49123e6d64"'   #Central_Reservation1_2_SQLDB_RI_31-05-2022
)

$ReservationsString=""
foreach($ReservationID in $ReservationIDs)
{
    if ( $ReservationsString -ne "" ) {
        $ReservationsString = -join("$ReservationsString", ",")
    }
    $ReservationsString = -join("$ReservationsString", "$ReservationID")
}


$csvPathAmortized = ("C:\BillingDetails\splitAmortizedres{0}.csv"-f $counter)
$Date = ((get-date).AddMonths($monthDelta))

$lastDay = [DateTime]::DaysInMonth($Date.Year, $Date.Month)
$firstDate = [DateTime]::new($Date.Year, $Date.Month, 1)
$lastDate  = [DateTime]::new($Date.Year, $Date.Month, $lastDay)


# SETTING UP the JSON FOR THE POST
$amortizedJsonPost = @"
{
    'type': 'AmortizedCost',
    'dataSet': {
        'granularity': 'None',
        'aggregation': {
            'totalCost': {
                'name': 'Cost',
                'function': 'Sum'
                }
        },
        'grouping': [
            {
                "type": "Dimension",
                "name": "SubscriptionId"
            },
            {
                "type": "Dimension",
                "name": "SubscriptionName"
            },
            {
                "type": "Dimension",
                "name": "MeterCategory"
            },
            {
                "type": "Dimension",
                "name": "MeterSubcategory"
            },
            {
                "type": "Dimension",
                "name": "ResourceGroupName"
            },
            {
                "type": "Dimension",
                "name": "ResourceId"
            },
            {
                "type": "Dimension",
                "name": "ResourceLocation"
            }
        ],
        'filter': {
            'Dimensions': {
                'Name': 'ReservationId',
                'Operator': 'In',
                'Values': [
                    $ReservationsString
                ]
            }
        }
    },
    'timeframe': 'Custom',
    'timePeriod': {
    'from': '$($firstDate.ToString("yyyy-MM-dd"))T00:00:00+00:00',
        'to': '$($lastDate.ToString("yyyy-MM-dd"))T23:59:59+00:00'
    }
}
"@

# -------------------------------------------------------
# DOWNLOAD CSV FROM EA PORTAL, AMORTIZED
# -------------------------------------------------------

Start-Sleep -Seconds 3
Write-Output "Gathering amortized billing Reports for Reservation: $ReservationID Month: $month to file: $csvPathAmortized ..."

$amortizedResponse = $null
$outputFile = "C:\path\to\outputfile.csv"
Invoke-WebRequest -Method Post -Headers $authHeader -Uri $urlAmortized -Body $amortizedJsonPost -ContentType application/json -OutFile $outputFile

# process response into a CSV file
$amoritzedArray = New-Object -TypeName System.Collections.ArrayList
$amoritzedArray.Add($amortizedResponse.properties.columns.name -join ";")
$amoritzedArray.AddRange($amortizedResponse.properties.rows.ForEach({$_ -join ";"}))
$amoritzedArray | ConvertFrom-CSV -Delimiter ";" | Select-Object -Property @{name="Abonnement-GUID (SubscriptionGuid)";expression={$($_.SubscriptionId)}}, @{name="Name des Abonnements (SubscriptionName)";expression={$($_.SubscriptionName.Split("(")[0])}}, @{name="Datum (Date)";expression={$($firstDate.ToString("yyyy-MM-dd"))}}, @{n="Kategorie der Verbrauchseinheit (MeterCategory)";expression={$($_.MeterCategory)}}, @{n="Unterkategorie der Verbrauchseinheit (MeterSubCategory)";expression={$($_.MeterSubCategory)+'-reservation'}}, @{name="Kosten (Cost)";expression={$($_.Cost)}}, @{name="ID der Instanz (InstanceId)";expression={$($_.ResourceId)}}, @{name="Ressourcengruppe (ResourceGroup)";expression={$($_.ResourceGroupName)}}, @{name="Ressourcenstandort (ResourceLocation)";expression={$($_.ResourceLocation)}} | ConvertTo-CSV | Out-File -FilePath "$csvPathAmortized" -Force -Encoding utf8
$counter = $counter +1

$filelist += $csvPathAmortized

# Removing amortized variables to free up memory
Remove-Variable amortizedJsonPost
Remove-Variable amoritzedArray
Remove-Variable amortizedResponse
[System.GC]::Collect()





# -------------------------------------------------------
# SPLIT FILES
# -------------------------------------------------------

foreach ($filename in $filelist) {
    #init variables
    $linecounter = 0 # remember the current line number
    $sentlines = 0 # remember how many lines are in the temporary chunk
    $loopcount = 0 # remember how many chunks we filled
    $chunksize = 100000 # max number of lines we add to each chunk
    $currentloopcount = -1 # remember the current chunk we work on to detect if it was rotated. Starting with -1 to make sure if differs from loopcount for the first run
    $header = "" # remember the header
    $headerfound=$false

    Write-Output "Working with file: $filename"
    Write-Output "Splitting file..."

    # read file line by line instead of consuming the whole file at once
    foreach ($line in [System.IO.File]::ReadLines($filename)) {

        # all lines after the header line have real content, so we have to send them to the current file and count how many we sent
        if ( $headerfound -eq $true ){

            # check if the loopcounter was increased. If yes, then the maximum lines for the last chunk are full
            if ( $currentloopcount -ne $loopcount) {

                # testing DB connection still works
                $sqlCommand = $sqlConnection.CreateCommand()
                $sqlCommand.CommandText = "SELECT * FROM dbo.BillingDetails2 WHERE 1 = 2"
                $sqlCommand.CommandTimeout = $timeout

                # writing the current temporary dataset (if existing) to the database temptable (as maximum lines were reached)
                if (Get-Variable 'dt' -Scope 'Global' -ErrorAction 'Ignore') {
                    Write-Output "Sending Info to DB temptable, $linecounter lines consumed so far..."
                    $bc = New-Object System.Data.SqlClient.SqlBulkCopy($sqlConnection, `
                        ([System.Data.SqlClient.SqlBulkCopyOptions]::TableLock -bor `
                                [System.Data.SqlClient.SqlBulkCopyOptions]::FireTriggers -bor `
                                [System.Data.SqlClient.SqlBulkCopyOptions]::UseInternalTransaction), `
                            $null )
                    $bc.DestinationTableName = $dt.TableName
                    $bc.BulkCopyTimeout = $timout
                    $bc.WriteToServer($dt);
                }

                # creating a temporary object to hold the info for the current chunk
                $dt = new-object System.Data.DataTable
                $adapter = new-object System.Data.SqlClient.SqlDataAdapter($sqlCommand)
                $adapter.Fill($dt)
                $dt.TableName = "dbo.BillingDetails2"

                # remember the name of the file we opened for the next iteration
                $currentloopcount = $loopcount
            }

            # create an array for the current line, which has the header and the current line we are working on
            $currentline = @()
            $currentline += "$header"
            $currentline += "$line"

            # converting the array into an object
            $currentobject = $currentline | convertfrom-csv

            # add the new line to the temporary dataset using the object we just created
            $row = $dt.NewRow()
            $row["SubscriptionGuid"] = [string] $currentobject."Abonnement-GUID (SubscriptionGuid)"
            $row["SubscriptionName"] = [string] $currentobject."Name des Abonnements (SubscriptionName)"
            $row["Date"] = [DateTime] $currentobject."Datum (Date)"
            $row["Month"] = [int]([DateTime] $currentobject."Datum (Date)").Month
            $row["Year"] = [int]([DateTime] $currentobject."Datum (Date)").Year
            $row["MeterCategory"] = [string] $currentobject."Kategorie der Verbrauchseinheit (MeterCategory)"
            $row["MeterSubCategory"] = [string] $currentobject."Unterkategorie der Verbrauchseinheit (MeterSubCategory)"
            $row["ExtendedCost"] = [decimal] $currentobject."Kosten (Cost)"
            $row["InstanceID"] = [string] $currentobject."ID der Instanz (InstanceId)"
            $row["ResourceGroup"] = [string] $currentobject."Ressourcengruppe (ResourceGroup)"
            $row["ResourceLocation"] = [string] $currentobject."Ressourcenstandort (ResourceLocation)"
            $dt.Rows.Add($row)

            # increase the counter for lines we added to the temporary dataset
            $sentlines += 1
        }

        # looking for the header
        if ( $headerfound -eq $false -and $null -ne $line ){
            $temparray=@()
            $temparray=$line.Split(',') -replace '"',''

            if ($temparray -contains "Abonnement-GUID (SubscriptionGuid)" -and
                $temparray -contains "Name des Abonnements (SubscriptionName)" -and
                $temparray -contains "Datum (Date)" -and
                $temparray -contains "Kategorie der Verbrauchseinheit (MeterCategory)" -and
                $temparray -contains "Unterkategorie der Verbrauchseinheit (MeterSubCategory)" -and
                $temparray -contains "Kosten (Cost)" -and
                $temparray -contains "ID der Instanz (InstanceId)" -and
                $temparray -contains "Ressourcengruppe (ResourceGroup)" -and
                $temparray -contains "Ressourcenstandort (ResourceLocation)")
            {
                Write-Output "found header. Saving it to fill it into each file"
                # initialize and remember the header
                $header = $line
                $headerfound=$true
            }
            Remove-Variable temparray
        }

        # if we reached the maximum amount of lines per chunk, then reset the counter and move to the next file
        if ( $sentlines -eq $chunksize){
            Write-Output "increasing loopcounter and reset sentlines"
            # increase the counter for which file should be used
            $loopcount += 1
            # Reset the counter for the sent lines
            $sentlines = 0
        }
        # move to the next line
        $linecounter += 1
    }

    # when the previous loop exited, there might be still information in the temporary object (dt). Sending this info to the DB
    if (Get-Variable 'dt' -Scope 'Global' -ErrorAction 'Ignore') {
        $bc = New-Object System.Data.SqlClient.SqlBulkCopy($sqlConnection, `
            ([System.Data.SqlClient.SqlBulkCopyOptions]::TableLock -bor `
                    [System.Data.SqlClient.SqlBulkCopyOptions]::FireTriggers -bor `
                    [System.Data.SqlClient.SqlBulkCopyOptions]::UseInternalTransaction), `
                $null )
        $bc.DestinationTableName = $dt.TableName
        $bc.BulkCopyTimeout = $timout
        $bc.WriteToServer($dt);

        Write-Output "Sent Info to DB temptable, consumed $linecounter lines in total"
        # removing some variables to free up memory
        Remove-Variable dt
        Remove-Variable bc
    }

    #Write-Output "deleting file $filename..."
    #Remove-Item $filename
}

[System.GC]::Collect()

# -------------------------------------------------------
# UPDATING Business Unit Info
# -------------------------------------------------------
Write-Output "Updating Business Unit Column 1/5"
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "UPDATE billingDetails2 SET BUnit=RIGHT(SubscriptionName, LEN(SubscriptionName) - (PATINDEX('%-BU-%', SubscriptionName)+3)) WHERE SubscriptionName LIKE '%-BU-%' AND BUnit IS NULL"
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()

Write-Output "Updating Business Unit Column 2/5"
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "UPDATE billingDetails2 SET BUnit='PROD' WHERE Lower(SubscriptionName) LIKE '%_prod' AND BUnit IS NULL"
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()

Write-Output "Updating Business Unit Column 3/5"
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "UPDATE billingDetails2 SET BUnit='INT' WHERE Lower(SubscriptionName) LIKE '%_int' AND BUnit IS NULL"
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()

Write-Output "Updating Business Unit Column 4/5"
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "UPDATE billingDetails2 SET BUnit='DEV' WHERE Lower(SubscriptionName) LIKE '%_dev' AND BUnit IS NULL"
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()

Write-Output "Updating Business Unit Column 5/5"
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "UPDATE billingDetails2 SET BUnit='Other' WHERE BUnit IS NULL"
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()

<#Write-Output "Updating Meter Category column value to Databricks in billingDetails2 having Databricks Reservation id '7383df3c-7cfc-455c-be69-cdd3bc86fe2f' in MeterSubCategory "
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "UPDATE billingDetails2 SET MeterCategory = 'Databricks Reservation' WHERE [MeterSubCategory] = '7383df3c-7cfc-455c-be69-cdd3bc86fe2f'"
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()


Write-Output "Updating Meter Category column value to Databricks in billingDetails2 having Databricks Reservation id '5d052853-b9d1-491a-acf0-667185a2ff28' in MeterSubCategory"
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "UPDATE billingDetails2 SET MeterCategory = 'Databricks Reservation' WHERE [MeterSubCategory] = '5d052853-b9d1-491a-acf0-667185a2ff28'"
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()
#>
Write-Output "Updating Meter Category column value to Databricks in billingDetails2 having Resource group name starting with 'Databricks-rg-*'"
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "UPDATE billingDetails2 SET MeterCategory = 'Azure Databricks' WHERE ResourceGroup Like 'databricks-rg-%'"
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()

Write-Output "Removing current monthly data"
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "DELETE FROM billingDetails_monthly WHERE YEAR = {0} AND MONTH = {1} " -f $year_todelete, $month_todelete
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()

Write-Output "Transfering new monthly data"
$sqlUpdateCommand = $sqlConnection.CreateCommand()
$sqlUpdateCommand.CommandText = "INSERT INTO [dbo].[billingDetails_monthly]  `
           ([SubscriptionGuid] `
           ,[SubscriptionName] `
           ,[Month] `
           ,[Year] `
           ,[MeterCategory] `
           ,[MeterSubCategory] `
           ,[ExtendedCost] `
           ,[InstanceID] `
           ,[ResourceGroup] `
           ,[BUnit] `
           ,[ResourceLocation]) `
	SELECT [SubscriptionGuid] `
           ,[SubscriptionName] `
           ,[Month] `
           ,[Year] `
           ,[MeterCategory] `
           ,[MeterSubCategory] `
           ,SUM([ExtendedCost]) `
           ,[InstanceID] `
           ,[ResourceGroup] `
           ,[BUnit] `
           ,[ResourceLocation] `
	FROM `
		billingDetails2 `
	WHERE [Year]={0} AND [Month]={1} `
	GROUP BY `
		[SubscriptionGuid] `
           ,[SubscriptionName] `
           ,[Month] `
           ,[Year] `
           ,[MeterCategory] `
           ,[MeterSubCategory] `
           ,[InstanceID] `
           ,[ResourceGroup] `
           ,[BUnit] `
           ,[ResourceLocation]" -f $year_todelete, $month_todelete
$sqlUpdateCommand.CommandTimeout = $timeout
$sqlUpdateCommand.ExecuteNonQuery()

Write-Output "Deleting old data in BillingDetails2 for: $year_todelete $month_todelete!"
$sqlDeleteCommand = $sqlConnection.CreateCommand()
$sqlDeleteCommand.CommandText = "DELETE FROM dbo.BillingDetails2 WHERE YEAR = {0} AND MONTH = {1} " -f $year_todelete, $month_todelete
$sqlDeleteCommand.CommandTimeout = $timeout
$sqlDeleteCommand.ExecuteNonQuery()

$sqlConnection.Close()
Write-Output "Done!"

# -------------------------------------------------------
# DELETE CSV
# -------------------------------------------------------

# Get-ChildItem "*.csv" | Remove-Item # no longer needed. There are no csv files generated for each chunk

#Write-Output "Removing downloaded file: $pathid"
#Remove-Item $pathid
