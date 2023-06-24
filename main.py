from flask import Flask
from requests import get
from bs4 import BeautifulSoup
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from extractors.jobkorea import extract_jobkorea_jobs
from file import save_to_file

# app = Flask("JobScrapper")
# app.run('0.0.0.0', port=5000, debug=True)
# @app.route("/")
# def home():
#     return 'hey there!'

wwr = extract_wwr_jobs("python")
indeed = extract_indeed_jobs("python")
jobkorea = extract_jobkorea_jobs("python")

jobs = wwr + indeed + jobkorea

save_to_file("./results/python_joblist1",jobs)