# Snowhitegirl1.github.io# Flask 잡 스크래퍼

3개의 웹사이트(Berlin Startup Jobs, WeWorkRemotely, Web3 Career)에서 채용 정보를 스크래핑하는 Flask 애플리케이션입니다.

---

## ⚠️ 중요: 실행 결과 (0 Jobs Found)에 대한 설명

이 프로젝트는 `requests`와 `BeautifulSoup`를 사용하여 3개의 사이트를 스크래핑하도록 설계되었습니다.

하지만 2025년 11월 현재, **3개의 대상 사이트가 모두 단순 HTTP 요청을 차단하는 강력한 봇(Bot) 방지 기술을 도입**하여, 현재 `requests` 라이브러리만으로는 데이터를 가져올 수 없습니다.

로컬에서 서버를 실행(`python main.py`)하고 검색하면, 터미널 로그와 함께 브라우저에 **`Found 0 jobs`**가 뜨는 것이 **정상적인(의도된) 실패**입니다.

### 각 사이트별 실패 원인 (터미널 로그)

1.  **WWR (WeWorkRemotely.com):**
    * **로그:** `WWR: Error during request: 403 Client Error: Forbidden...`
    * **원인:** `User-Agent` 헤더를 포함했음에도 불구하고, 서버가 `requests` 라이브러리의 접근을 봇으로 탐지하고 `403 Forbidden` (접근 거부) 에러를 반환합니다.

2.  **Web3 Career:**
    * **로그:** `Web3: FAILED. This site loads jobs dynamically (JavaScript).`
    * **원인:** `requests`는 HTML 뼈대만 가져옵니다. 이 사이트는 JavaScript가 나중에 데이터를 동적으로 불러오는 방식(Dynamic Loading)을 사용하므로, `requests`는 텅 빈 페이지만 보게 됩니다. (이를 해결하려면 Selenium/Playwright 같은 브라우저 자동화 도구가 필요합니다.)

3.  **Berlin Startup Jobs:**
    * **로그:** `Berlin: Container has 1 potential job items.` -> `Berlin: Found 0 valid jobs.`
    * **원인:** 가장 교묘한 방식으로, 서버가 `requests`의 접근을 탐지하고 브라우저에게 보내는 "진짜" 직업 목록 대신, 아이템이 1개뿐인 **"가짜"(Decoy) HTML**을 보냅니다. 스크래퍼는 이 가짜 목록을 분석하지만 유효한 직업을 찾지 못해 0개를 반환합니다.

---

## 로컬에서 실행 방법 (How to Run Locally)

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/(YourID)/(YourID).github.io.git](https://github.com/(YourID)/(YourID).github.io.git)
    cd (YourID).github.io
    ```

2.  **Install dependencies:**
    ```bash
    pip install flask requests beautifulsoup4
    ```

3.  **Run the Flask server:**
    ```bash
    python main.py
    ```

4.  **Open your browser:**
    브라우저에서 `http://127.0.0.1:5000` 주소로 접속하면 로컬 스크래퍼가 실행됩니다. (결과는 0이 나옵니다.)