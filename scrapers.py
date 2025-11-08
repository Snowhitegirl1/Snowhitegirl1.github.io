# scrapers.py
import requests
from bs4 import BeautifulSoup

# [수정됨] 403 에러는 어쩔 수 없지만, 헤더는 유지합니다.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1' 
}

def scrape_berlin_startup_jobs(term):
    """berlinstartupjobs.com 스크래퍼 (최종 수정)"""
    url = f"https://berlinstartupjobs.com/skill-areas/{term}/"
    print(f"Scraping Berlin Startup Jobs: {url}")
    jobs_db = []
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # -----------------------------------------------------------------
        # ▼▼▼ 여기가 수정되었습니다 ▼▼▼
        # 'find' 대신 'find_all'을 사용해 모든 'jobs-list-items' 목록을 가져옵니다.
        list_containers = soup.find_all("ul", class_="jobs-list-items")
        # ▲▲▲ 여기가 수정되었습니다 ▲▲▲

        if not list_containers:
            print("Berlin: No job list containers (ul.jobs-list-items) found at all.")
            return jobs_db
        
        print(f"Berlin: Found {len(list_containers)} list container(s).")
        
        # 페이지에 있는 모든 목록 컨테이너를 순회합니다.
        for container in list_containers:
            # 각 목록 안의 모든 <li> 태그를 찾습니다.
            jobs_in_container = container.find_all("li")
            print(f"Berlin: Container has {len(jobs_in_container)} potential job items.")

            for job in jobs_in_container:
                # <li> 태그 안에 제목/회사 클래스가 있는지 확인합니다.
                title_h4 = job.find("h4", class_="bjs-jlid_h")
                link_tag = title_h4.find("a") if title_h4 else None
                company_tag = job.find("a", class_="bjs-jlid_b")
                
                # 두 요소가 모두 있어야 실제 공고로 간주합니다.
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
                    if job_data not in jobs_db: # 중복 방지
                        jobs_db.append(job_data)
        
        print(f"Berlin: Finished parsing. Found {len(jobs_db)} valid jobs.")
                
    except requests.exceptions.RequestException as e:
        print(f"Berlin: Error: {e}")
    except AttributeError as e:
        print(f"Berlin: Error parsing HTML: {e}")
        
    return jobs_db

def scrape_web3_career(term):
    """web3.career 스크래퍼 (동적 로딩으로 스크래핑 불가능)"""
    url = f"https://web3.career/{term}-jobs"
    print(f"Scraping Web3 Career: {url}")
    
    # 이 사이트는 JavaScript로 데이터를 동적 로딩하므로
    # requests/BeautifulSoup 방식으로는 스크래핑이 불가능합니다.
    print("Web3: FAILED. This site loads jobs dynamically (JavaScript).")
    print("      Cannot scrape with current method. Skipping...")
    
    return [] # 빈 리스트 반환

def scrape_weworkremotely(term):
    """weworkremotely.com 스크래퍼 (403 Forbidden으로 차단됨)"""
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={term}"
    print(f"Scraping WeWorkRemotely: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status() # 403 에러가 뜨는지 여기서 다시 확인
        
        # (만약 403을 통과했다면 아래 코드가 실행되지만, 지금은 차단되어 실행되지 않음)
        soup = BeautifulSoup(response.text, "html.parser")
        jobs_section = soup.find("section", id="category-2")
        
        if not jobs_section:
            print("WWR: No job section container (section#category-2) found.")
            return []
            
        jobs = jobs_section.find_all("li", class_="new-listing-container")
        # (이하 생략...)

    except requests.exceptions.RequestException as e:
        # 403 에러가 발생하면 여기가 실행됩니다.
        print(f"WWR: Error during request: {e}")
        print("      Site is actively blocking scraper. Skipping...")
    except Exception as e:
        print(f"WWR: Error: {e}")
        
    return [] # 빈 리스트 반환