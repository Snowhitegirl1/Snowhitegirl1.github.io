# Snowhitegirl1.github.io# Flask 잡 스크래퍼

3개의 웹사이트(Berlin Startup Jobs, WeWorkRemotely, Web3 Career)에서 채용 정보를 스크래핑하는 Flask 애플리케이션입니다.

---

## ⚠️ 실행 전 참고

이 프로젝트는 Python Flask를 사용하는 **동적(Dynamic) 웹 애플리케이션**입니다.

이 저장소는 `github.io` 페이지 배포를 위해 사용되며, `index.html` 파일은 프로젝트 안내를 위한 정적 랜딩 페이지입니다.

**Flask 스크래퍼를 실행하려면 반드시 로컬 환경에서 Python을 직접 실행해야 합니다.**

---

## 로컬에서 실행 방법 (How to Run Locally)

1.  **Clone this repository (or download ZIP):**
    ```bash
    git clone [https://github.com/Snowhitegirl1/Snowhitegirl1.github.io.git](https://github.com/Snowhitegirl1/Snowhitegirl1.github.io.git)
    cd Snowhitegirl1.github.io
    ```

2.  **Install dependencies:**
    (이 프로젝트는 `flask`, `requests`, `beautifulsoup4`가 필요합니다.)
    ```bash
    pip install flask requests beautifulsoup4
    ```

3.  **Run the Flask server:**
    ```bash
    python main.py
    ```

4.  **Open your browser:**
    브라우저에서 `http://127.0.0.1:5000` 주소로 접속하면 로컬에서 실행되는 스크래퍼를 확인할 수 있습니다.