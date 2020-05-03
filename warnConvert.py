#! /usr/bin/env python3

import os
import requests
import subprocess
import tabula
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

url = "https://www.illinoisworknet.com/LayoffRecovery/Pages/ArchivedWARNReports.aspx"

#If there is no such folder, the script will create one automatically
folder_location = r'/Users/vincent/Projects/WARN/WARNReports'
Path(folder_location).mkdir(parents=True, exist_ok=True)

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")     
for link in soup.select("a[href$='.pdf']"):
    #Names the pdf files using the last portion of each link which are unique in this case
    filename = os.path.join(folder_location,link['href'].split('/')[-1])
    #If there is no such file, the script will create one automatically
    if not os.path.exists(filename):
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url,link['href'])).content)

#Goes through each file in the folder and converts them to a csv file
for filename in os.listdir(r'/Users/vincent/Projects/WARN/WARNReports'):
    print(filename)
    #Exclude hidden files
    if not filename.startswith('.'):
        try:
            tabula.read_pdf(filename, pages='all')
            tabula.convert_into(filename, filename[:-4] + ".csv", output_format="csv", pages='all')
        except subprocess.CalledProcessError as e:
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
