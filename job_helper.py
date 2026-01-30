def extract_job_and_employment_type(job_header):
    """
    Extracts job title and employment type from a single <h4> job element.

    Args:
        job_header: BeautifulSoup <h4> element

    Returns:
        dict: Contains "Title" and "Employment Type"
    """
    text = job_header.text.strip()
    
    # Determine employment type
    if text.endswith("Full Time"):
        employment_type = "Full Time"
        title = text.rsplit("Full Time", 1)[0].strip()
    elif text.endswith("Part Time"):
        employment_type = "Part Time"
        title = text.rsplit("Part Time", 1)[0].strip()
    elif text.endswith("Any"):
        employment_type = "Any"
        title = text.rsplit("Any", 1)[0].strip()
    else:
        employment_type = "Other"
        title = text
    
    return {
        "title": title,
        "employment_type": employment_type
    }


def extract_posted_local(date_tag):
    """
    Extracts the local posted date/time from a <p> tag containing data-temp.

    Args:
        date_tag (bs4.element.Tag): The <p> tag with attributes like data-temp

    Returns:
        str: Posted date/time as string in format "YYYY-MM-DD HH:MM:SS", or "N/A" if not found
    """
    if date_tag:
        posted_local = date_tag.get('data-temp')  # extract local time
        return posted_local if posted_local else "N/A"
    return "N/A"

def extract_job_description(desc_div):
    """
    Extracts the job description text from a <div> containing the job snippet.

    Args:
        desc_div (bs4.element.Tag): The <div> element containing the job description

    Returns:
        str: Job description text (without the "See More" link)
    """
    if not desc_div:
        return "N/A"

    # Get all text nodes in the div, stripping extra whitespace
    text_parts = [t.strip() for t in desc_div.strings if t.strip()]

    # Remove the "See More" text if present
    if text_parts and text_parts[-1] == "See More":
        text_parts = text_parts[:-1]

    # Join all parts into a single string
    description = " ".join(text_parts)
    return description


def extract_job_link(desc_div, base_url="https://www.onlinejobs.ph"):
    """
    Extracts the job link from the <div> containing the job description.

    Args:
        desc_div (bs4.element.Tag): The div containing the job description
        base_url (str): The website base URL to make the link absolute

    Returns:
        str: Full URL to the job page, or "N/A" if not found
    """
    if not desc_div:
        return "N/A"

    link_tag = desc_div.find('a', href=True)
    if link_tag:
        href = link_tag['href']
        # Convert relative URL to full URL
        if href.startswith("/"):
            return base_url + href
        return href
    return "N/A"

