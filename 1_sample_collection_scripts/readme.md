This folder contains the script used to download the goodware and some ransomware samples. 

The `software_informer_scraper.py` script is used to download the goodware samples while the `virusshare_scraper.py` is used to download some of the ransomware samples. Details about these codes can be found below and in the code itself. 


# `software_informer_scraper.py`

A Python scraper that downloads goodware samples from [Software Informer](https://software.informer.com/software/) and also gathers metadata (e.g., download links, file sizes, MD5 hashes) about the samples. Requires ~100GB free disk space for the full dataset. Therefore, ensure you have disk space before running the code. 

## Prerequisites
- **Python 3.x**
- **Packages**: `requests`, `beautifulsoup4`, `pandas`, `tqdm`  
  ```bash
  pip install requests beautifulsoup4 pandas tqdm
  ```

## Usage
1. **Clone** this repository:
   ```bash
   git clone https://github.com/faithfulco/mlran/1_sample_collection_scripts.git
   cd software-informer-scraper
   ```
2. **Run** the scraper:
   ```bash
   python software_informer_scraper.py
   ```
   - Creates a `downloads` folder (if not present).
   - Saves metadata to `application_data.csv`.
   - Downloads software installers locally.

## Code Overview

- **`get_soup(url)`**  
  Returns a BeautifulSoup object from a given URL or `None` if requests fail.

- **`scrape_application_page(app_url)`**  
  Scrapes details (filename, size, MD5, last checked date, direct download link) for an app.

- **`download_file(url, file_name)`**  
  Downloads a file in chunks to `downloads/`. Prints an error on failure.

- **`scrape_page(page_number)`**  
  Scrapes all apps on a specified page, calling `download_file` and `scrape_application_page` for each item.

- **`application_data`**  
  A global list storing metadata (`title`, `description`, `href`, `File`, `Size`, `MD5`, `Last checked`, `Download link`) for each scraped application.


# `virusshare_scraper.py`

This Jupyter Notebook contains code to access the [VirusShare](https://virusshare.com/) website and automatically download malicious samples. The scraper automates interactions with the VirusShare platform, making it easier to retrieve and manage sample datasets for cybersecurity research and analysis.

## Features
- Automatically logs into VirusShare.
- Searches and retrieves malicious file samples by hash.
- Saves the downloaded samples securely into a designated folder.
- Includes safeguards and best practices for handling malicious files.

## Usage
1. **Environment Setup**:
   - Ensure you run this notebook in a secure and isolated environment, such as a virtual machine, to prevent accidental infections.
   - Install required Python libraries such as `requests` and `BeautifulSoup`.

2. **Execution**:
   - Update the code with your VirusShare credentials.
   - Specify the list of hashes you wish to search for.
   - Run the cells in sequence to perform the scraping and download process.

3. **File Management**:
   - Downloaded samples are saved in the `sample_download` folder for organized storage.

## Ethical Considerations
Downloading and handling malicious samples come with ethical and legal responsibilities. Always ensure:
- Compliance with VirusShare’s terms of service and policies.
- Adherence to broader cybersecurity ethics.
- Proper precautions to isolate and secure the downloaded samples.

**Caution**: VirusShare archives files with the password `infected` for security. Do not attempt to extract or execute these files outside a secure environment.


---

