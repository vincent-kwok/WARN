#! /usr/bin/env python3

import glob
import os
import pandas
import re
import requests
import tabula
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

url = "https://www.illinoisworknet.com/LayoffRecovery/Pages/ArchivedWARNReports.aspx"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

#If there is no folder named WARNReports, then the script will create one
Path('./WARNReports/').mkdir(exist_ok=True)
os.chdir('./WARNReports/')

#Parse and iterate the webpage for links ending with .pdf
for link in soup.select("a[href$='.pdf']")[:100]:
    #Name the pdf files using the last portion of each link which are unique in this case
    filename = re.sub(r'\D+$', '', link['href'].split('/')[-1].replace('%20', '')) + ".pdf"
    #If there is no csv with that filename, then the script will create one
    if not glob.glob(filename[:-4] + '*'):
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url, link['href'])).content)
            print('Created ' + filename)

#Convert files in folder to a csv file
for pdfFile in os.listdir():
    #Exclude hidden files
    if pdfFile[-3:] == 'pdf':
        tabula.read_pdf(pdfFile, multiple_tables=True, pages = 'all', pandas_options={'header':None})
        tabula.convert_into(pdfFile, pdfFile[:-4] + '.csv', output_format='csv', pages='all')
        print('Deleted ' + pdfFile)
        os.remove(pdfFile)

#Combine all csvs in year into a xlsx file
for year in range(2012, 2020+1):
    writer = pandas.ExcelWriter(str(year) + '.xlsx')
    files = glob.glob('[a-zA-Z]*' + str(year) + '.{}'.format('csv'))
    tableList = []
    for csvs in files:
        df = pandas.read_csv(csvs, header=None, names=[0,1,2,3,4,5,6])
        tableList.append(df)
    frame = pandas.concat(tableList, axis=0, ignore_index=True)
    frame.to_excel(writer, str(year), index=False)
    writer.save()
