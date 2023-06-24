from requests import get
from bs4 import BeautifulSoup
import json

def extract_jobkorea_jobs(keyword):
    base_url = "https://www.jobkorea.co.kr/Search/?stext="        
    response = get(f"{base_url}{keyword}")    

    results = []

    if response.status_code != 200:
        print("Cant request website")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all('div', class_ = "list-default")


        for job_section in jobs:        
            job_posts = job_section.find_all('li', class_ = "list-post")            
            for post in job_posts:
                link = post['data-gavirturl']
                # data-gainfo 속성 값 가져오기                
                data_gainfo = post['data-gainfo']   
                
                # 딕셔너리로 변환
                info_dict = json.loads(data_gainfo)

                # 딕셔너리 값 활용
                company = info_dict['dimension48']
                location = info_dict['dimension46']
                title = info_dict['dimension45']
                
                job_data ={
                    'link': link.replace("virtual/", ""),
                    'company':company.replace(",", " "),                                           
                    'location': location.replace(",", " "),                                           
                    'position':title.replace(",", " "),                                                               
                }
                results.append(job_data)
                print(job_data)
    
    return results

