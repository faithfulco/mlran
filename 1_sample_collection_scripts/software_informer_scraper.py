# Import packages
import requests
from requests.exceptions import TooManyRedirects
from bs4 import BeautifulSoup
import os
import pandas as pd
from tqdm import tqdm
import time

# Create a folder downloads to store all the software to be downloaded. 
download_suffix = "download"

# Headers to be sent with requests to mimic a real browser
# You can find this through the developer tools in your browser. 
# E.g. for chrome, click on inspect, then click on network, then refresh page, click on any aspect, and you'll see Request Headers.
headers = {
    'Referer': 'https://software.informer.com/software/',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# Create the downloads directory if it does not exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

def get_soup(url):
    """Fetch the content from the URL and return a BeautifulSoup object."""
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except TooManyRedirects:
        print(f"Too many redirects for URL: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for URL: {url}, Error: {e}")
        return None

def scrape_application_page(app_url):
    """Scrape application details from the application page."""
    app_soup = get_soup(app_url + download_suffix)
    if app_soup is None:
        return None, None, None, None, None
    
    try:
        # The idea here is to only extract softwares that have an anti-virus check report. 
        report_link_tag = app_soup.find('a', string='see the report')
        if report_link_tag is None:
            print(f"No report link found for {app_url}. Skipping...")
            return None, None, None, None, None
        
        report_link = report_link_tag.get('href')
        if not report_link:
            print(f"No valid report link found for {app_url}. Skipping...")
            return None, None, None, None, None
        
        report_soup = get_soup(report_link)
        if report_soup is None:
            print(f"Error getting report soup for {report_link}. Skipping...")
            return None, None, None, None, None
        
        file_info = report_soup.find('p', class_='file_info').find_all('span')
        file_name = file_info[0].text.split(': ')[1]
        file_size = file_info[1].text.split(': ')[1]
        file_md5 = file_info[2].text.split(': ')[1]
        last_checked = file_info[3].text.split(': ')[1]

        # Find the download link. We extract this from the href of the "Download Now" button.
        download_link_tag = app_soup.find('a', class_='download_btn')
        download_link = download_link_tag['href'] if download_link_tag else None
        if not download_link:
            print(f"No download link found for {app_url}. Skipping...")
            return None, None, None, None, None
            
        return file_name, file_size, file_md5, last_checked, download_link
    except Exception as e:
        print(f"Error scraping {app_url}: {e}")
        return None, None, None, None, None

def download_file(url, file_name):
    """Download the file from the given URL and save it to the 'downloads' directory."""
    try:
        # Send the GET request with the specified headers
        response = requests.get(url, headers=headers, stream=True)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Open the file in the 'downloads' directory with the specified file name
        with open(f'downloads/{file_name}', 'wb') as f:
            # Iterate over the response content in chunks of 8192 bytes
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    f.write(chunk)
                    
    except requests.exceptions.TooManyRedirects:
        # Handle too many redirects error
        print(f"Too many redirects for URL: {url}. Skipping download...")
    except requests.exceptions.RequestException as e:
        # Handle other request-related errors
        print(f"Error downloading {url}: {e}")

def scrape_page(page_number):
    """Scrape all applications on a given page. The link is for the Most popular software for Windows. You can change this link to download different categories of samples."""
    url = f"https://software.informer.com/software/{page_number}/"
    soup = get_soup(url)
    if soup is None:
        print(f"Error getting soup for page {page_number}. Skipping...")
        return
    
    apps = soup.find_all('a', class_='link_ttl')
    for app in apps:
        app_href = app['href']
        app_title = app.text.strip()
        app_description_tag = app.find_next('div', class_='description')
        if not app_description_tag:
            app_description_tag = app.find_next('p')
        app_description = app_description_tag.text.strip() if app_description_tag else "No description available"
        
        file_name, file_size, file_md5, last_checked, download_link = scrape_application_page(app_href)
        if file_name and file_size and file_md5 and last_checked and download_link:
            download_file(download_link, file_name)
            # Extract the following information for the given software to be downloaded. 
            application_data.append({
                "title": app_title,
                "description": app_description,
                "href": app_href,
                "File": file_name,
                "Size": file_size,
                "MD5": file_md5,
                "Last checked": last_checked,
                "Download link": download_link
            })

application_data = []

# Scrape the pages with a progress bar. The pages are up to 300. Most popular software for Windows. 
for page in tqdm(range(1, 301), desc="Scraping pages"):
    scrape_page(page)
    time.sleep(1)  # to prevent being blocked by the server

# Save the scraped data to a CSV file
df = pd.DataFrame(application_data)
df.to_csv('application_data.csv', index=False)
print("Scraping completed and data saved to application_data.csv")
print("Scraping completed and software saved in downloads folder.")