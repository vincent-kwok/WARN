#! /usr/bin/env python3

import os
import requests
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup

url = "https://www.illinoisworknet.com/LayoffRecovery/Pages/ArchivedWARNReports.aspx"

#If there is no such folder, the script will create one automatically
folder_location = r'/Users/vincent/Projects/WARN/WARNReports'
Path(folder_location).mkdir(parents=True, exist_ok=True)

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")     
for link in soup.select("a[href$='.pdf']"):
    #Name the pdf files using the last portion of each link which are unique in this case
    filename = os.path.join(folder_location,link['href'].split('/')[-1])
    #If there is no such file, the script will create one automatically
    if not os.path.exists(filename):
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url,link['href'])).content)

