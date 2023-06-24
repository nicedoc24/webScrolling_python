from requests import get
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(options=options)

def get_page_count(keyword):
    base_url = "https://kr.indeed.com/jobs"        
    browser.get(f"{base_url}?q={keyword}&limit50")
    soup = BeautifulSoup(browser.page_source, "html.parser")    
    paginations = soup.find("nav", attrs={"aria-label": "pagination"})
    #print(len(paginations))
    pages = paginations.find_all("div", recursive=False)
    count = (len(pages)) # 페이지의 갯수
    
    if count == 0:
        return 1    
    elif count >= 5:
        return 5
    else:
        return count-1  #>화살표 제거    
    print(count)


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    base_url = "https://kr.indeed.com/jobs"
    results = [] # 값을 저장할 list
    print("Found", pages, "pages")
    for page in range(pages):        
        final_url = (f"{base_url}?q={keyword}&start={page*10}&limit50")
        print("Requesting", final_url)
        browser.get(final_url)

        # 해당 사이트가 봇으로 인식해서 막고있으므로, requests로 상태코드 확인 불가
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_ = "jobsearch-ResultsList")
        jobs = job_list.find_all('li', recursive=False) # ul 바로 아래 li만 찾기 위해 recursive 옵션 False 값 줌.
        for job in jobs :    
            zone = job.find("div", class_="mosaic-zone")
            if zone == None: # 아무 내용 없는 요소 제거
                anchor = job.select_one("h2 a")
                # h2 = job.find("h2", class_="jobTitle")
                # a = h2.find("a")
                # [1] 제목(직책)
                title = anchor['aria-label']
                # [2] 링크
                link = anchor['href']               
                # [3] 회사명
                company = job.find("span", class_="companyName")
                # [4] 지역
                location = job.find("div", class_="companyLocation")
                
                job_data ={
                    'link': f"https://www.indeed.com{link}",
                    'company':company.string.replace(",", " "),                                           
                    'location': location.string.replace(",", " "),                                           
                    'position':title.replace(",", " "),                                                               
                }
                results.append(job_data)
        # for result in results:
        #     print(result, "\n===========================================\n")    
    return results

