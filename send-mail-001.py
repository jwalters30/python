import json
import msal

import requests

client_id = 'yyy'
client_secret = 'xxx'
tenant_id = 'xxx'
authority = f"https://login.microsoftonline.com/{tenant_id}"

app = msal.ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority)

scopes = ["https://graph.microsoft.com/.default"]

result = None
result = app.acquire_token_silent(scopes, account=None)

if not result:
    print(
        "No suitable token exists in cache. Let's get a new one from Azure Active Directory.")
    result = app.acquire_token_for_client(scopes=scopes)

# if "access_token" in result:
#     print("Access token is " + result["access_token"])


if "access_token" in result:
    userId = "jwalters@go-planet.com"
    endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/sendMail'
    toUserEmail = "jwalters@go-planet.com"
    email_msg = {'Message': {'Subject': "Test Sending Email from Python",
                             'Body': {'ContentType': 'Text', 'Content': "This is a test email."},
                             'ToRecipients': [{'EmailAddress': {'Address': toUserEmail}}]
                             },
                 'SaveToSentItems': 'true'}
    r = requests.post(endpoint,
                      headers={'Authorization': 'Bearer ' + result['access_token']}, json=email_msg)
    if r.ok:
        print('Sent email successfully')
    else:
        print(r.json())
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))