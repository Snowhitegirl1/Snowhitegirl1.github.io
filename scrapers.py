# scrapers.py
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5.3.6 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/5.3.6'
}

def scrape_berlin_startup_jobs(term):
    """berlinstartupjobs.com에서 채용 정보 스크래핑 (수정된 버전)"""
    url = f"https://berlinstartupjobs.com/skill-areas/{term}/"
    print(f"Scraping Berlin Startup Jobs: {url}")
    jobs_db = []
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 'jobs-list-items' ul 태그는 그대로입니다.
        jobs_list = soup.find("ul", class_="jobs-list-items")
        
        if not jobs_list:
            print("Berlin: No job list container (ul.jobs-list-items) found.")
            return jobs_db

        # 'job-listing' 클래스 대신 'bjs-jlid' 클래스를 찾습니다.
        jobs = jobs_list.find_all("li", class_="bjs-jlid")
        
        print(f"Berlin: Found {len(jobs)} job list items.") # 디버깅용 로그

        for job in jobs:

            # 'job-title' 클래스 대신 'bjs-jlid_h' 내부의 <a> 태그를 찾습니다.
            title_h4 = job.find("h4", class_="bjs-jlid_h")
            link_tag = title_h4.find("a") if title_h4 else None
            
            # 'company-name-link' 클래스 대신 'bjs-jlid_b' 클래스를 찾습니다.
            company_tag = job.find("a", class_="bjs-jlid_b")
        
            
            # 필수 요소가 모두 있는지 확인
            if link_tag and company_tag:
                link = link_tag["href"]
                title = link_tag.get_text(strip=True)
                company = company_tag.get_text(strip=True)
                
                job_data = {
                    "site": "Berlin Startup Jobs",
                    "title": title,
                    "company": company,
                    "link": link
                }
                jobs_db.append(job_data)
            else:
                # 스크래핑 실패 시 로그 (어떤 태그를 놓쳤는지 확인용)
                if not link_tag:
                    print("Berlin: Could not find link_tag (h4.bjs-jlid_h > a)")
                if not company_tag:
                    print("Berlin: Could not find company_tag (a.bjs-jlid_b)")

    except requests.exceptions.RequestException as e:
        print(f"Berlin: Error during request: {e}")
    except AttributeError as e:
        print(f"Berlin: Error parsing HTML (likely structure changed): {e}")
        
    return jobs_db

def scrape_web3_career(term):
    """web3.career에서 채용 정보 스크래핑 (수정된 버전)"""
    url = f"https://web3.career/{term}-jobs"
    print(f"Scraping Web3 Career: {url}")
    jobs_db = []

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        

        # <table> 대신, id가 'job_'으로 시작하는 모든 <div>를 찾습니다.
        # (lambda는 간단한 함수를 만드는 파이썬 문법입니다)
        jobs = soup.find_all("div", id=lambda x: x and x.startswith("job_"))
    
        
        print(f"Web3: Found {len(jobs)} job list items.") # 디버깅용 로그
        
        for job in jobs:
            
            # 'job_title' 클래스 대신 'text-lg'와 'font-bold'를 포함하는 <a> 태그를 찾습니다.
            link_tag = job.find("a", class_=lambda c: c and "text-lg" in c and "font-bold" in c)
            
            # 'job_company' 클래스 대신 'text-black-alpha-50'을 포함하는 <a> 태그를 찾습니다.
            company_tag = job.find("a", class_=lambda c: c and "text-black-alpha-50" in c)
            

            if link_tag and company_tag:
                link = "https://web3.career" + link_tag["href"]
                title = link_tag.get_text(strip=True)
                company = company_tag.get_text(strip=True)
                
                job_data = {
                    "site": "Web3 Career",
                    "title": title,
                    "company": company,
                    "link": link
                }
                jobs_db.append(job_data)
            else:
                 if not link_tag:
                    print("Web3: Could not find link_tag (a.text-lg.font-bold)")
                 if not company_tag:
                    print("Web3: Could not find company_tag (a.text-black-alpha-50)")

    except requests.exceptions.RequestException as e:
        print(f"Web3: Error during request: {e}")
    except AttributeError as e:
        print(f"Web3: Error parsing HTML: {e}")
        
    return jobs_db

def scrape_weworkremotely(term):
    """weworkremotely.com에서 채용 정보 스크래핑 (수정된 버전)"""
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={term}"
    print(f"Scraping WeWorkRemotely: {url}")
    jobs_db = []

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 'category-2' ID를 가진 section
        jobs_section = soup.find("section", id="category-2")
        
        if not jobs_section:
            print("WWR: No job section container (section#category-2) found.")
            return jobs_db
            
        # 'new-listing-container' 클래스를 찾습니다.
        jobs = jobs_section.find_all("li", class_="new-listing-container")
        
        print(f"WWR: Found {len(jobs)} job list items.") # 디버깅용 로그

        for job in jobs:
            
            # 제목, 회사, 링크가 모두 <a> 태그 안에 포함되어 있습니다.
            link_tag = job.find("a", class_="listing-link__unlocked")
            
            # <a> 태그가 없는 li (예: 'view all' 버튼)는 건너뜁니다.
            if not link_tag:
                continue

            # <a> 태그 안에서 제목과 회사 이름을 찾습니다.
            title_tag = link_tag.find("h3", class_="new-listing_header_title")
            company_tag = link_tag.find("p", class_="new-listing_company-name")
            
            
            if title_tag and company_tag:
                link = "https://weworkremotely.com" + link_tag["href"]
                title = title_tag.get_text(strip=True)
                company = company_tag.get_text(strip=True)
                
                job_data = {
                    "site": "WeWorkRemotely",
                    "title": title,
                    "company": company,
                    "link": link
                }
                jobs_db.append(job_data)
            else:
                if not title_tag:
                    print("WWR: Could not find title_tag (h3.new-listing_header_title)")
                if not company_tag:
                    print("WWR: Could not find company_tag (p.new-listing_company-name)")

    except requests.exceptions.RequestException as e:
        print(f"WWR: Error during request: {e}")
    except (AttributeError, IndexError) as e:
        print(f"WWR: Error parsing HTML: {e}")
        
    return jobs_db