import os
import requests
import logging
import http.client

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

http.client.HTTPConnection.debuglevel = 1

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

url = "https://www.eventbriteapi.com/v3/users/me/"
auth = {"Authorization": "Bearer " + os.getenv("EVENTBRITE_TOKEN")}

with requests.Session() as session:
    session.headers = auth
    response = session.get(url)
    print(response.text)
