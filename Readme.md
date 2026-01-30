# OLJ Web Scraper

A Python scraper for [OnlineJobs.ph](https://www.onlinejobs.ph) that extracts job listings and saves them as Excel files organized by posted date.

---

## Features

- Scrapes job listings including:
  - Job Title
  - Employment Type (Full Time, Part Time, Any, Other)
  - Company / Institution
  - Location
  - Posted Date (Local Time)
  - Job Description
  - Job Link
- Automatically creates a `data/` folder and saves each day’s listings in an Excel file named `YYYY-MM-DD.xlsx`.
- Handles missing fields gracefully.
- Uses helper functions for modular and maintainable code.

---

## Folder Structure

```
OLJ-WebScraping/
│
├─ job_helper.py         # Contains all helper functions
├─ scrape_jobs.py        # Main scraper script
├─ data/                 # Folder where Excel files are saved
└─ README.md             # This file
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/OLJ-WebScraping.git
cd OLJ-WebScraping
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

> If you don’t have a `requirements.txt`, you can install manually:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

---

## Usage

1. Open `scrape_jobs.py`.
2. Run the script:

```bash
python scrape_jobs.py
```

3. The script will scrape the latest jobs and save them in `data/YYYY-MM-DD.xlsx`.

---

## Helper Functions

All scraping logic is modularized in `job_helper.py`, including:

- `extract_job_and_employment_type(job_header)` – Extracts title and employment type from `<h4>` tags.
- `extract_posted_local(date_tag)` – Extracts the posted date from a `<p>` tag.
- `extract_job_description(desc_div)` – Extracts the job description text.
- `extract_job_link(desc_div)` – Extracts the job link from the description `<div>`.

---

## Notes

- The scraper works with the HTML structure of OnlineJobs.ph as of Jan 2026. Changes to the site may require updates to selectors.
- Currently, the scraper cannot extract the “who posted” field because it is dynamically loaded via JavaScript.
- Excel files are overwritten if they exist for the same date. You can modify the script to append instead.

License

This project is open-source and free to use under the MIT License.