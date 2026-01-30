import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import job_helper
from datetime import datetime

# URL of the job board page
url = "https://www.onlinejobs.ph/jobseekers/jobsearch"

# Send a GET request to fetch the page
response = requests.get(url)

# Parse the content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find all job listings
job_listings = soup.find_all('div', class_='jobpost-cat-box')

# Prepare a list to store all job data
all_jobs = []

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


    # Save each job as a dictionary
    all_jobs.append({
        "Title": job_info['title'],
        "Employment Type": job_info['employment_type'],
        "Posted Local": posted_time,
        "Description": description,
        "Link": job_link
    })

# If no jobs found, exit
if not all_jobs:
    print("No jobs found.")
    exit()

# Create the folder if it doesn't exist
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

# Use the date from the first job to name the Excel file
first_date = all_jobs[0]['Posted Local']
if first_date != "N/A":
    file_date = datetime.strptime(first_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
else:
    file_date = datetime.now().strftime("%Y-%m-%d")

excel_path = os.path.join(output_folder, f"{file_date}.xlsx")

# Convert to pandas DataFrame and save as Excel
df = pd.DataFrame(all_jobs)
df.to_excel(excel_path, index=False)

print(f"Saved {len(all_jobs)} jobs to {excel_path}")
