# scrapers.py
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5.3.6 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/5.3.6'
}

def scrape_berlin_startup_jobs(term):
    """berlinstartupjobs.com에서 채용 정보 스크래핑"""
    url = f"https://berlinstartupjobs.com/skill-areas/{term}/"
    print(f"Scraping Berlin Startup Jobs: {url}")
    jobs_db = []

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        jobs_list = soup.find("ul", class_="jobs-list-items")

        if not jobs_list:
            return jobs_db

        jobs = jobs_list.find_all("li", class_="job-listing")

        for job in jobs:
            link_tag = job.find("h4", class_="job-title").find("a")
            company_tag = job.find("a", class_="company-name-link")

            if link_tag and company_tag:
                job_data = {
                    "site": "Berlin Startup Jobs",
                    "title": link_tag.get_text(strip=True),
                    "company": company_tag.get_text(strip=True),
                    "link": link_tag["href"]
                }
                jobs_db.append(job_data)
    except Exception as e:
        print(f"Berlin: Error: {e}")
    return jobs_db

def scrape_web3_career(term):
    """web3.career에서 채용 정보 스크래핑"""
    url = f"https://web3.career/{term}-jobs"
    print(f"Scraping Web3 Career: {url}")
    jobs_db = []

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find("tbody").find_all("tr", class_="table_row")

        for job in jobs:
            if not job.find("td", class_="job_title"):
                continue

            link_tag = job.find("td", class_="job_title").find("a")
            company_tag = job.find("td", class_="job_company").find("a")

            if link_tag and company_tag:
                job_data = {
                    "site": "Web3 Career",
                    "title": link_tag.get_text(strip=True),
                    "company": company_tag.get_text(strip=True),
                    "link": "https://web3.career" + link_tag["href"]
                }
                jobs_db.append(job_data)
    except Exception as e:
        print(f"Web3: Error: {e}")
    return jobs_db

def scrape_weworkremotely(term):
    """weworkremotely.com에서 채용 정보 스크래핑"""
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={term}"
    print(f"Scraping WeWorkRemotely: {url}")
    jobs_db = []

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        jobs_section = soup.find("section", id="category-2")

        if not jobs_section:
            return jobs_db

        jobs = jobs_section.find_all("li", class_="feature")

        for job in jobs:
            if job.find("span", class_="title") and job.find("span", class_="company"):
                link_tag = job.find_all("a")[1]
                job_data = {
                    "site": "WeWorkRemotely",
                    "title": job.find("span", class_="title").get_text(strip=True),
                    "company": job.find("span", class_="company").get_text(strip=True),
                    "link": "https://weworkremotely.com" + link_tag["href"]
                }
                jobs_db.append(job_data)
    except Exception as e:
        print(f"WWR: Error: {e}")
    return jobs_db