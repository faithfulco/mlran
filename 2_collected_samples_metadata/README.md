## File Descriptions

### 1. `goodware_samples_description.csv`

This file contains metadata about **goodware** samples that were gathered from [software informer](https://software.informer.com/) for this research.

#### **Columns**

1. **sample_id**  
   - Numeric ID to uniquely identify each sample.  
2. **filename**  
   - The original file name of the software installer or executable.  
3. **md5**  
   - MD5 hash of the file.  
4. **title**  
   - Name or title of the software.  
5. **description**  
   - Short description of the software’s functionality.  
6. **type**  
   - Category or classification from the source website (e.g., `most_popular`).  
7. **href**  
   - URL to the software’s page on software.informer (or related site).  
8. **size**  
   - File size (often in MB).  
9. **download_link**  
   - Link to directly download the installer or executable.  
10. **last_checked**  
   - Date indicating when the link or metadata was last verified.

---
### 2. `ransomware_samples_families_description.csv`

This file contains descriptive information about **ransomware families**. It’s useful for mapping **family names** to their **types**, **years**, and additional resources or references.

#### **Columns**

1. **family**  
   - Name of the ransomware family (e.g., `blackbasta`, `wannacry`, `reveton`).  
2. **type**  
   - Ransomware type (e.g., `locker`, `crypto`, `raas`, `modern`).  
3. **year**  
   - Year of initial discovery or major outbreak.  
4. **description**  
   - Brief summary of the ransomware’s behaviour, infection vector, or notable characteristics.  
5. **family_label**  
   - Numeric label for the `family`.  
6. **type_label**  
   - Numeric label for the ransomware type (e.g., `1` for locker, `2` for crypto, `3` for raas, `4` for modern).  
7. **links**  
   - Reference links for more information (e.g., security research articles).
  
---
### 3. `mlran_dataset_metadata.csv`

This file contains the metadata of the **MLRan dataset**. It includes metadata that correlates **sample IDs** to cryptographic hashes, classification labels (e.g. ransomware vs. goodware) and other metadata. 

#### **Columns**

1. **sample_id**  
   - A unique numeric identifier for each sample (ransomware or goodware).
   - Ransomware samples start at 10,001; goodware samples start at 13,000.
2. **sha256**  
   - SHA-256 hash of the sample.  
3. **sample_type**  
   - Indicates whether the sample is goodware or ransomware (`0` for goodware and `1` for ransomware).  
4. **ransomware_family**  
   - The family name if it’s a ransomware sample; `0` if goodware.  
5. **family_label**  
   - A numeric label for the ransomware family (e.g., `0` for goodware). Converted from the `ransomware_family` column. 
6. **ransomware_type**  
   - Type of ransomware (e.g., `crypto`, `locker`, etc.); goodware samples are named `goodware`.  
7. **type_label**  
   - Numeric label indicating the ransomware type (e.g., `0` for goodware, `1` for locker, `2` for crypto, `3` for raas, `4` for modern).  
8. **sha1**  
   - SHA-1 hash of the file.  
9. **md5**  
   - MD5 hash of the file (matches the `md5` in `goodware_samples_description.csv` if it’s a goodware).  
10. **extension**  
    - File extension.  
11. **detections**  
    - Indicates how many antivirus engines flagged the file as malicious out of the total scanned by VirusTotal (e.g., `0/77` means no detections among 77 engines).  
    - All goodware samples have `0`, while ransomware samples have at least one detection.
12. **timestamp**  
    - A timestamp related to when the sample was first seen or analyzed. 
13. **source**  
    - Indicates where each sample originated.  
    - Goodware: All goodware samples were downloaded from [software informer website](https://software.informer.com/). The label indicates the category of the sample (e.g., `most_popular`, `developer_tools`, `communications`).  
    - Ransomware: Collected from multiple sources:  
      1. **elderan** – [GitHub](https://github.com/rissgrouphub/ransomwaredataset2016)  
      2. **motif** – [GitHub](https://github.com/boozallen/MOTIF)  
      3. **marauder** – [GitHub](https://github.com/THU-WingTecher/MarauderMap)  
      4. **curated** – Aggregated from platforms like Malware Bazaar, Ransomware Reports etc.

---
