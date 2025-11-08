# main.py
from flask import Flask, render_template, request, redirect, url_for
from scrapers import scrape_berlin_startup_jobs, scrape_web3_career, scrape_weworkremotely

app = Flask(__name__)

# 임시 캐시
db = {}

@app.route("/")
def home():
    """홈페이지, 검색 폼을 렌더링합니다."""
    # Flask는 templates 폴더 안의 index.html을 찾습니다.
    return render_template("index.html")

@app.route("/search")
def search():
    """
    검색어를 받아 스크래핑을 수행하고 결과를 렌더링합니다.
    """
    term = request.args.get('term')

    if not term or not term.strip():
        return redirect(url_for("home"))

    term = term.lower()

    if term in db:
        jobs = db[term]
    else:
        berlin_jobs = scrape_berlin_startup_jobs(term)
        web3_jobs = scrape_web3_career(term)
        wwr_jobs = scrape_weworkremotely(term)
        jobs = berlin_jobs + web3_jobs + wwr_jobs
        db[term] = jobs

    total_jobs = len(jobs)

    # Flask는 templates 폴더 안의 search.html을 찾습니다.
    return render_template("search.html", 
                           term=term, 
                           total_jobs=total_jobs, 
                           jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)