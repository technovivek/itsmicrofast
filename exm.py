import json

import requests

# url = "https://api.powerbi.com/v1.0/myorg/gateways/2048c04b-ccdd-46a9-9a7b-07b5fabb838f/datasources"
# host = "adb-8085862804474344.4.azuredatabricks.net"
# kind = "Databricks"
# body = {
#     "datasourceName": "datab02",
#     "datasourceType": "Extension",
#     "connectionDetails": "{\"extensionDataSourceKind\":\"f\"{}\",\"extensionDataSourcePath\":\"{\\\"host\\\":\\\"adb-8085862804474344.4.azuredatabricks.net\\\",\\\"httpPath\\\":\\\"\\\\/sql\\\\/1.0\\\\/endpoints\\\\/0fb64603abbafd22\\\"}\"}",
#     "credentialDetails": {
#         "encryptedConnection": "Encrypted",
#         "credentials": "FVECb/lru81kzbe/lPcJXa/hptz632vLlnJOCO3MgKNZVvDClhAeL+xWM0ODEJMm2TryqKBDvTtVT4vKoAAA2t18rNP1QJIrMCYBihYsMDy+uIytsRYEarMKvgsEFPzbaqh7AsQLa3WXNDPS8G8gMCAXm+8z30ta+TJK5h/JrNsgfJH1C1N0h0HngxSsfpxVl2iQwrVzUSLd5fsXw0C9yJIC3nzbHeZK1LfSSyOV8dexcl9XNJia7zYETWh+q0gGdQ/IzY1LKhAXsX93+M5HUvRcpfeoufvc3Ev/pMsoWdIYIVXRrwzufkUl5Q7SuwOLkoHutUBFWJoo/Vh/9/zTew==AAC20FIwJzt9STv4gSt5H0/QB1Ym38O2PQvb2PJNXLD4oyREZDyTeA4blh7ZAIDWcL3CsU82nRr2rH7puEORgb6yMfuaYHdY8BjmA1sjbhqPZEZeyDTPdbjFWnELexYCDz19oI5yyMwARrjZCfmjgfQZ1+7M7gdgbG9o33kP7fXnR6MDD/DByyq4DslPNTyMYPM=",
#         "credentialType": "Key",
#         "privacyLevel": "Organizational",
#         "encryptionAlgorithm": "RSA-OAEP"
#     }
# }
# headers = {"Content-Type": "application/json","Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvOTY1MmQ3YzItMWNjZi00OTQwLTgxNTEtNGE5MmJkNDc0ZWQwLyIsImlhdCI6MTY5MTEzNTA1OCwibmJmIjoxNjkxMTM1MDU4LCJleHAiOjE2OTExMzk5MjIsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVlFBcS84VUFBQUFUc3hwNS9ONkxucDdmalJGTmxMMFAvODZaR1kzTjdzdDh1OXkxN3ZQQy9XWnBhQlJudUJ3c1JGak9lQmFiVFBZdnZIcWtEdUx0VGt0cVZrc1czVndBNXhCSDlvajcrMGVCYzR4b1U5NjJvUT0iLCJhbXIiOlsibWZhIl0sImFwcGlkIjoiMThmYmNhMTYtMjIyNC00NWY2LTg1YjAtZjdiZjJiMzliM2YzIiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJLdW1hciIsImdpdmVuX25hbWUiOiJWaXZlayIsImlwYWRkciI6IjE2My4xMTYuMTk5LjEyMCIsIm5hbWUiOiJLdW1hciwgVml2ZWsgVi4gKDYyMykiLCJvaWQiOiI0NDI3ODUyOS1mYjkxLTQ5YjgtOTAwMS02ZjE4N2E5ZDlkNTEiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMTIxNDQ0MDMzOS0xNzE1NTY3ODIxLTgzOTUyMjExNS03NTYzODQiLCJwdWlkIjoiMTAwMzIwMDFDQTg4RUE0QiIsInJoIjoiMC5BUUlBd3RkU2xzOGNRRW1CVVVxU3ZVZE8wQWtBQUFBQUFBQUF3QUFBQUFBQUFBQUNBQUkuIiwic2NwIjoiQXBwLlJlYWQuQWxsIENhcGFjaXR5LlJlYWQuQWxsIENhcGFjaXR5LlJlYWRXcml0ZS5BbGwgQ29udGVudC5DcmVhdGUgRGFzaGJvYXJkLlJlYWQuQWxsIERhc2hib2FyZC5SZWFkV3JpdGUuQWxsIERhdGFmbG93LlJlYWQuQWxsIERhdGFmbG93LlJlYWRXcml0ZS5BbGwgRGF0YXNldC5SZWFkLkFsbCBEYXRhc2V0LlJlYWRXcml0ZS5BbGwgR2F0ZXdheS5SZWFkLkFsbCBHYXRld2F5LlJlYWRXcml0ZS5BbGwgUGlwZWxpbmUuRGVwbG95IFBpcGVsaW5lLlJlYWQuQWxsIFBpcGVsaW5lLlJlYWRXcml0ZS5BbGwgUmVwb3J0LlJlYWQuQWxsIFJlcG9ydC5SZWFkV3JpdGUuQWxsIFN0b3JhZ2VBY2NvdW50LlJlYWQuQWxsIFN0b3JhZ2VBY2NvdW50LlJlYWRXcml0ZS5BbGwgVGVuYW50LlJlYWQuQWxsIFRlbmFudC5SZWFkV3JpdGUuQWxsIFVzZXJTdGF0ZS5SZWFkV3JpdGUuQWxsIFdvcmtzcGFjZS5SZWFkLkFsbCBXb3Jrc3BhY2UuUmVhZFdyaXRlLkFsbCIsInN1YiI6ImNqbVJpc25pWkJiZjNPclktaWtSazl4TjBYWFVqVEFmS3dtZ0poN2dKS1kiLCJ0aWQiOiI5NjUyZDdjMi0xY2NmLTQ5NDAtODE1MS00YTkyYmQ0NzRlZDAiLCJ1bmlxdWVfbmFtZSI6Imt1bXZpdkBhcGFjLmNvcnBkaXIubmV0IiwidXBuIjoia3Vtdml2QGFwYWMuY29ycGRpci5uZXQiLCJ1dGkiOiJzaWVqTTVNZVZFU0tRVl9lRmtrV0FBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJhOWVhODk5Ni0xMjJmLTRjNzQtOTUyMC04ZWRjZDE5MjgyNmMiLCJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXX0.gBd8_RtrE9EiEtKR7qbybxO3lrUIfMxI299kXyN1NXQtVhej3xH9Khq38Z8_ZF3Ys4hNyO3bj8CbkG_Ul6mXyx48ruzXWsnk4e8ttFV6KSpTTwb5b7DEVWXykrWQVg71lWC50iF4naBXsGtVMMTIVkaXt5fhB2U1E4XbB3zxBi3iCZz2fIcYmvFqAqMPlDKJV1CEZboTNle8JHsVyZ0YK0E19rZFwrCscZ2opFieOMvez7Lrpp2Q5bquwMpiTonjEFDhZShq-3BUhDf5atSiN-yzotzUSNIvYvFcxV7yXuBH2agS6S7it22jssc04Cve7_h9l-69YmOo56bv35E_Iw"}
#
# res = requests.post(url = url, data=  json.dumps(body), headers=headers, verify= False)
#
# res.raise_for_status()
# print(res.json())
import requests
# from azure.identity import DefaultAzureCredential
from azure.identity import ClientSecretCredential
AUTHORITY_URL = "https://login.microsoftonline.com/"
PBI_TENANT_ID = "9652d7c2-1ccf-4940-8151-4a92bd474ed0"
PBI_APP_ID = "daf5850e-9a49-4379-b0c9-44285ed32437"
PBI_CLIENT_SECRET = "bL88Q~OpGXqXj.koUxNZj1p-QAAX5Oegkb3KEaaC~"

PBI_API = "https://analysis.windows.net/powerbi/api/.default"
def get_access_token() -> str:
    auth = ClientSecretCredential(
        authority=AUTHORITY_URL,
        tenant_id=PBI_TENANT_ID,
        client_id=PBI_APP_ID,
        client_secret=PBI_CLIENT_SECRET,
    )
    access_token = auth.get_token(PBI_API)
    access_token = access_token.token
    return access_token


# access_token = get_access_token()
# print("Access token:", access_token)
# Replace with your subscription ID and resource ID for Databricks SQL
subscription_id = PBI_TENANT_ID
databricks_sql_resource_id = "0fb64603abbafd22"

# API endpoint to get information about a specific resource
api_version = "2021-05-01-preview"  # Replace with the appropriate API version

resource_url = f"https://management.azure.com/subscriptions/{subscription_id}/resources/{databricks_sql_resource_id}?api-version={api_version}"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvOTY1MmQ3YzItMWNjZi00OTQwLTgxNTEtNGE5MmJkNDc0ZWQwLyIsImlhdCI6MTY5MTIxOTc3MiwibmJmIjoxNjkxMjE5NzcyLCJleHAiOjE2OTEyMjQxOTcsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVlFBcS84VUFBQUFmdktmVzN3Y3JYRDFUSVY4aHhrSUw0K2hSZTJjMVdsbzB2cVFZdTFuaUlTaFFaSWlSbFdvdzQ0Y3JtYnEwMGxVdE9HdVRxRUxvV0duMnVKMVJhdmJEYWovazVhMVVtTDFydGZjTGdINk1BQT0iLCJhbXIiOlsibWZhIl0sImFwcGlkIjoiMThmYmNhMTYtMjIyNC00NWY2LTg1YjAtZjdiZjJiMzliM2YzIiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJLdW1hciIsImdpdmVuX25hbWUiOiJWaXZlayIsImlwYWRkciI6IjE2My4xMTYuMTk2LjQzIiwibmFtZSI6Ikt1bWFyLCBWaXZlayBWLiAoNjIzKSIsIm9pZCI6IjQ0Mjc4NTI5LWZiOTEtNDliOC05MDAxLTZmMTg3YTlkOWQ1MSIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS0xMjE0NDQwMzM5LTE3MTU1Njc4MjEtODM5NTIyMTE1LTc1NjM4NCIsInB1aWQiOiIxMDAzMjAwMUNBODhFQTRCIiwicmgiOiIwLkFRSUF3dGRTbHM4Y1FFbUJVVXFTdlVkTzBBa0FBQUFBQUFBQXdBQUFBQUFBQUFBQ0FBSS4iLCJzY3AiOiJBcHAuUmVhZC5BbGwgQ2FwYWNpdHkuUmVhZC5BbGwgQ2FwYWNpdHkuUmVhZFdyaXRlLkFsbCBDb250ZW50LkNyZWF0ZSBEYXNoYm9hcmQuUmVhZC5BbGwgRGFzaGJvYXJkLlJlYWRXcml0ZS5BbGwgRGF0YWZsb3cuUmVhZC5BbGwgRGF0YWZsb3cuUmVhZFdyaXRlLkFsbCBEYXRhc2V0LlJlYWQuQWxsIERhdGFzZXQuUmVhZFdyaXRlLkFsbCBHYXRld2F5LlJlYWQuQWxsIEdhdGV3YXkuUmVhZFdyaXRlLkFsbCBQaXBlbGluZS5EZXBsb3kgUGlwZWxpbmUuUmVhZC5BbGwgUGlwZWxpbmUuUmVhZFdyaXRlLkFsbCBSZXBvcnQuUmVhZC5BbGwgUmVwb3J0LlJlYWRXcml0ZS5BbGwgU3RvcmFnZUFjY291bnQuUmVhZC5BbGwgU3RvcmFnZUFjY291bnQuUmVhZFdyaXRlLkFsbCBUZW5hbnQuUmVhZC5BbGwgVGVuYW50LlJlYWRXcml0ZS5BbGwgVXNlclN0YXRlLlJlYWRXcml0ZS5BbGwgV29ya3NwYWNlLlJlYWQuQWxsIFdvcmtzcGFjZS5SZWFkV3JpdGUuQWxsIiwic3ViIjoiY2ptUmlzbmlaQmJmM09yWS1pa1JrOXhOMFhYVWpUQWZLd21nSmg3Z0pLWSIsInRpZCI6Ijk2NTJkN2MyLTFjY2YtNDk0MC04MTUxLTRhOTJiZDQ3NGVkMCIsInVuaXF1ZV9uYW1lIjoia3Vtdml2QGFwYWMuY29ycGRpci5uZXQiLCJ1cG4iOiJrdW12aXZAYXBhYy5jb3JwZGlyLm5ldCIsInV0aSI6InpoRU1jRDJHZVVtVUxWb2N1WjRMQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImE5ZWE4OTk2LTEyMmYtNGM3NC05NTIwLThlZGNkMTkyODI2YyIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdfQ.Un_F5UDMO6h5DU-nQpNxboi7jsnJIfsPt7o0ZRv3ya5VOr7ygFRZuzvd3gDKvaba8OCbTy44D3FqD3MyWOenAA3tVEAtRzT3ICVEZVH1Ks1NnH7Kaej_njK-7rEAdN3uRhcNVzFkuP3UA6p05Fj-38pkn2NGyd0ZumUBezzfI4zKeY5BPgtdfoBIpRinQ4oThcM0g-BzqHZaNarGVCXLD0AuA__su9ljCTH16lThRB6rxereMCKFqZoyR1C3uSxoQQcGE8mPjqxwtqAcNrIzpUTFlD47ksOcyht4ipMQC0lN3z7tZEdm0AMWodkkLdSfzdsEbjleKwTbImSxQhGkyQ"
# Send the request
response = requests.get(resource_url, headers={"Authorization": f"Bearer {token}"})

# Check the response
if response.status_code == 200:
    resource_data = response.json()
    print("Databricks SQL Warehouse Information:")
    print(resource_data)
else:
    print(f"Failed to retrieve Databricks SQL information. Status code: {response.status_code}")
    print(response.text)