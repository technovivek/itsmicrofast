



#az login #has to run for the first run
$response= az account get-access-token
$token=$response | convertfrom-json | select-object -ExpandProperty accessToken

$authHeader = @{
'Content-Type'  = 'application/json'
'Authorization' = 'Bearer ' + ($token)
}

$monthDelta=0
$Date = ((get-date).AddMonths($monthDelta))

$lastDay = [DateTime]::DaysInMonth($Date.Year, $Date.Month)
$firstDate = [DateTime]::new($Date.Year, $Date.Month, 1)
$lastDate  = [DateTime]::new($Date.Year, $Date.Month, $lastDay)
$urlAmortized = 'https://management.azure.com/providers/Microsoft.Management/managementGroups/eXtollo_production/providers/Microsoft.CostManagement/query?api-version=2019-11-01'

#### this part is new for dynamically getting the reservation IDs ####

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
               "name": "ReservationId"
           }
       ],
     "filter":{
        "dimensions":{
           "name":"PricingModel",
           "operator":"In",
           "values":[
              "reservation"
           ]
        }
     },
       }
   },
   'timeframe': 'Custom',
   'timePeriod': {
   'from': '$($firstDate.ToString("yyyy-MM-dd"))T00:00:00+00:00',
       'to': '$($lastDate.ToString("yyyy-MM-dd"))T23:59:59+00:00'
   }
}
"@




$amortizedResponse = $null
$amortizedResponse = Invoke-RestMethod -Method Post -Headers $authHeader -Uri $urlAmortized -Body $amortizedJsonPost -ContentType application/json

# process response into a CSV file
$amoritzedArray = New-Object -TypeName System.Collections.ArrayList
$amoritzedArray.Add($amortizedResponse.properties.columns.name -join ";")
$amoritzedArray.AddRange($amortizedResponse.properties.rows.ForEach({$_ -join ";"}))


write-output "####"
$ReservationIDs = $amoritzedArray | ConvertFrom-CSV -Delimiter ";" | select-object -expandproperty ReservationId

$ReservationsString=""
foreach($ReservationID in $ReservationIDs)
{
   if ( $ReservationsString -ne "" ) {
       $ReservationsString = -join("$ReservationsString", ",")
   }
   $ReservationsString = -join("$ReservationsString", "`"$ReservationID`"")
}


Write-output "$ReservationsString"

write-output "####"


#### this part is to toy around with the JSON
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


#$amortizedJsonPost = @"
#{
#    'type': 'AmortizedCost',
#    'dataSet': {
#        'granularity': 'None',
#        'aggregation': {
#            'totalCost': {
#                'name': 'Cost',
#                'function': 'Sum'
#                }
#        },
#        'grouping': [
#            {
#                "type": "Dimension",
#                "name": "SubscriptionId"
#            },
#            {
#                "type": "Dimension",
#                "name": "SubscriptionName"
#            },
#            {
#                "type": "Dimension",
#                "name": "MeterCategory"
#            },
#            {
#                "type": "Dimension",
#                "name": "MeterSubcategory"
#            },
#            {
#                "type": "Dimension",
#                "name": "ResourceGroupName"
#            },
#            {
#                "type": "Dimension",
#                "name": "ResourceId"
#            },
#            {
#                "type": "Dimension",
#                "name": "ResourceLocation"
#            }
#        ],
#        'filter': {
#            'Dimensions': {
#                'Name': 'ReservationId',
#                'Operator': 'In',
#                'Values': [
#                    $ReservationsString
#                ]
#            },
#            "dimensions":{
#            "name":"PricingModel",
#            "operator":"In",
#            "values":[
#               "reservation"
#            ]
#         }
#        }
#    },
#    'timeframe': 'Custom',
#    'timePeriod': {
#    'from': '$($firstDate.ToString("yyyy-MM-dd"))T00:00:00+00:00',
#        'to': '$($lastDate.ToString("yyyy-MM-dd"))T23:59:59+00:00'
#    }
#}
#"@

$amortizedResponse = $null
$amortizedResponse = Invoke-RestMethod -Method Post -Headers $authHeader -Uri $urlAmortized -Body $amortizedJsonPost -ContentType application/json

# process response into a CSV file
$amoritzedArray = New-Object -TypeName System.Collections.ArrayList
$amoritzedArray.Add($amortizedResponse.properties.columns.name -join ";")
$amoritzedArray.AddRange($amortizedResponse.properties.rows.ForEach({$_ -join ";"}))

$amoritzedArray | ConvertFrom-CSV -Delimiter ";" | Select-Object -Property @{name="Abonnement-GUID (SubscriptionGuid)";expression={$($_.SubscriptionId)}}, @{name="Name des Abonnements (SubscriptionName)";expression={$($_.SubscriptionName.Split("(")[0])}}, @{name="Datum (Date)";expression={$($firstDate.ToString("yyyy-MM-dd"))}}, @{n="Kategorie der Verbrauchseinheit (MeterCategory)";expression={$($_.MeterCategory)}}, @{n="Unterkategorie der Verbrauchseinheit (MeterSubCategory)";expression={$($_.MeterSubCategory)}}, @{name="Kosten (Cost)";expression={$($_.Cost)}}, @{name="ID der Instanz (InstanceId)";expression={$($_.ResourceId)}}, @{name="Ressourcengruppe (ResourceGroup)";expression={$($_.ResourceGroupName)}}, @{name="Ressourcenstandort (ResourceLocation)";expression={$($_.ResourceLocation)}} | ConvertTo-CSV #| Out-File -FilePath "$csvPathAmortized" -Force -Encoding utf8