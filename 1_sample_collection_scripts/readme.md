This folder contains the script used to download the goodware and some ransomware samples. 


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
