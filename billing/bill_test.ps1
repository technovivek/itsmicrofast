$url = "https://dummyjson.com/products/1"
$csvoutputFile = "C:\Users\kumviv\OneDrive - Mercedes-Benz (corpdir.onmicrosoft.com)\pythonProject\mock_test\billing\output.csv"
$jsonoutputFile = "C:\Users\kumviv\OneDrive - Mercedes-Benz (corpdir.onmicrosoft.com)\pythonProject\mock_test\billing\output.json"



Invoke-WebRequest -Method Get $url -ContentType application/json -OutFile $jsonoutputFile
Write-Host "Response dumped to json"

Write-Host "Generating a csv file"

# Read the JSON file
$jsonData = Get-Content -Raw -Path $jsonoutputFile

# Convert JSON to PowerShell objects
$jsonObjects = $jsonData | ConvertFrom-Json

# Export PowerShell objects to CSV file
$jsonObjects | Export-Csv -Path $csvoutputFile -NoTypeInformation