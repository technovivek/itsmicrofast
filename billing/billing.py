import requests
from datetime import datetime, timedelta

# Authenticate and get access token
url_login = "https://login.microsoftonline.com/<tenant_id>/oauth2/token"
headers_login = {"Content-Type": "application/x-www-form-urlencoded"}
data_login = {
    "grant_type": "client_credentials",
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "resource": "https://management.azure.com/"
}
response_login = requests.post(url_login, headers=headers_login, data=data_login)
access_token = response_login.json()["access_token"]

# Prepare headers for API requests
auth_header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Set the month delta and calculate dates
month_delta = 0
date = datetime.now() + timedelta(months=month_delta)
last_day = date.replace(day=1, month=date.month+1, day=1) - timedelta(days=1)
first_date = date.replace(day=1)
last_date = last_day.replace(hour=23, minute=59, second=59)

# Get reservation IDs
url_amortized = "https://management.azure.com/providers/Microsoft.Management/managementGroups/eXtollo_production/providers/Microsoft.CostManagement/query?api-version=2019-11-01"
amortized_payload = {
    "type": "AmortizedCost",
    "dataSet": {
        "granularity": "None",
        "aggregation": {
            "totalCost": {
                "name": "Cost",
                "function": "Sum"
            }
        },
        "grouping": [
            {
                "type": "Dimension",
                "name": "ReservationId"
            }
        ],
        "filter": {
            "dimensions": {
                "name": "PricingModel",
                "operator": "In",
                "values": ["reservation"]
            }
        }
    },
    "timeframe": "Custom",
    "timePeriod": {
        "from": f"{first_date.isoformat()}",
        "to": f"{last_date.isoformat()}"
    }
}

response_amortized = requests.post(url_amortized, headers=auth_header, json=amortized_payload)
reservation_ids = [row["ReservationId"] for row in response_amortized.json()["properties"]["rows"]]

reservations_string = ",".join(f'"{reservation_id}"' for reservation_id in reservation_ids)

# Get amortized costs for each reservation
amortized_payload["dataSet"]["grouping"] = [
    {"type": "Dimension", "name": "SubscriptionId"},
    {"type": "Dimension", "name": "SubscriptionName"},
    {"type": "Dimension", "name": "MeterCategory"},
    {"type": "Dimension", "name": "MeterSubcategory"},
    {"type": "Dimension", "name": "ResourceGroupName"},
    {"type": "Dimension", "name": "ResourceId"},
    {"type": "Dimension", "name": "ResourceLocation"}
]
amortized_payload["dataSet"]["filter"] = {
    "Dimensions": {
        "Name": "ReservationId",
        "Operator": "In",
        "Values": reservation_ids
    }
}
amortized_payload["timePeriod"] = {
    "from": f"{first_date.isoformat()}",
    "to": f"{last_date.isoformat()}"
}

response_amortized = requests.post(url_amortized, headers=auth_header, json=amortized_payload)

# Process response into a CSV-like format
amortized_data = response_amort
