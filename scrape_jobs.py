import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import job_helper
from datetime import datetime
import time

# Base URL of the job board
BASE_URL = "https://www.onlinejobs.ph/jobseekers/jobsearch"

# Folder to save Excel files
OUTPUT_FOLDER = "data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Start scraping
all_jobs = []

# First request to get the pagination info
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Find last page number from pagination
pagination = soup.find("ul", class_="pagination")
if pagination:
    page_links = pagination.find_all("a", {"data-ci-pagination-page": True})
    last_page_number = max(int(a["data-ci-pagination-page"]) for a in page_links)
else:
    last_page_number = 1  # Only 1 page

print(f"Total pages detected: {last_page_number}")

# Loop through all pages
for page in range(1, last_page_number + 1):
    print(f"Scraping page {page}...")
    if page == 1:
        url = BASE_URL
    else:
        offset = (page - 1) * 30  # 30 jobs per page
        url = f"{BASE_URL}/{offset}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_listings = soup.find_all('div', class_='jobpost-cat-box')
    if not job_listings:
        print(f"No jobs found on page {page}, stopping.")
        break

    for job in job_listings:
        # Extract job title and employment type
        job_header = job.find('h4', class_='fs-16 fw-700')
        job_info = job_helper.extract_job_and_employment_type(job_header)

        # Extract posted date
        date_tag = job.find('p', class_='fs-13 mb-0')
        posted_time = job_helper.extract_posted_local(date_tag)

        # Extract job description
        desc_div = job.find('div', class_='desc fs-14 d-none d-sm-block')
        description = job_helper.extract_job_description(desc_div)

        # Extract job link
        job_link = job_helper.extract_job_link(desc_div)
        

        all_jobs.append({
            "Title": job_info['title'],
            "Employment Type": job_info['employment_type'],
            "Posted Local": posted_time,
            "Description": description,
            "Link": job_link
        })

    time.sleep(1)  # polite delay to avoid being blocked

# Save all jobs to Excel
if not all_jobs:
    print("No jobs found overall.")
else:
    # Use the date from the first job to name the Excel file
    first_date = all_jobs[0]['Posted Local'] if all_jobs else "N/A"
    if first_date != "N/A":
        file_date = datetime.strptime(first_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    else:
        file_date = datetime.now().strftime("%Y-%m-%d")

    excel_path = os.path.join(OUTPUT_FOLDER, f"{file_date}.xlsx")
    df = pd.DataFrame(all_jobs)
    df.to_excel(excel_path, index=False)

    print(f"Saved {len(all_jobs)} jobs to {excel_path}")
