#This code will get sections 1 and 7A from the lastest 10k SEC filings for a company and store it in Google Datastore. It tries to collect up to a decade of data.
from sec_api import QueryApi, ExtractorApi
import csv
import sys
from bs4 import BeautifulSoup
from google.cloud import datastore
from SECAPI10kToCSV import recent10K
# This API requires a key. The SEC EDGAR API is free but the text/html files are extremely difficult to extract certain sections from due to variation in how companies structure their filings.
KEY = "YOUR KEY"
myExtractor = ExtractorApi(KEY)
myQuery = QueryApi(api_key = KEY)
datastore_client = datastore.Client()
def collect(ticker):
    tenK = recent10K(ticker)
    toDatastore(ticker, tenK)

def toDatastore(ticker, filings):
    filing_url = filings["linkToFilingDetails"]
    section_text = myExtractor.get_section(filing_url, "1A", "text")
    section_html = myExtractor.get_section(filing_url, "7", "html")
    soup = BeautifulSoup(section_html, 'html.parser')
    section_text_html_stripped = soup.get_text()
    # The kind for the new entity
    kind = '10k_company_data'
    # The name/ID for the new entity
    name = ticker + " data" + filings["filedAt"][0:4]
    # The Cloud Datastore key for the new entity
    task_key = datastore_client.key(kind, name)
    # Prepares the new entity
    task = datastore.Entity(key=task_key,exclude_from_indexes= ['Section 1A', 'Section 7'])
    task['Date of 10k Filing'] = filings["filedAt"]
    task['Section 1A'] = section_text
    task['Section 7'] = section_text_html_stripped
    task['Ticker/Company'] = ticker
    # Saves the entity
    print("data saving now...")
    datastore_client.put(task)

if __name__ == "__main__":
    collect(sys.argv[1])




