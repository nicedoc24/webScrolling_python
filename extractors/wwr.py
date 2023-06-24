from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="        
    response = get(f"{base_url}{keyword}")    

    if response.status_code != 200:
        print("Cant request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all('section', class_ = "jobs")
        for job_section in jobs:\
        
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]     # 두번째 anchor 값이 유효한 값이기에 해당값만 저장.
                link = anchor['href']   # anchor 값이 dic이기 때문에 href 값을 link로 저장해줌.
                company, kind, region = anchor.find_all('span', class_ ="company") # list의 모든 값을 순서대로 저장해 줌. (list의 수를 아는 경우)
                title = anchor.find('span', class_ = "title")
                job_data ={
                    'link': f"https://weworkremotely.com{link}",
                    'company':company.string.replace(","," "),                                           
                    'location':region.string.replace(","," "),
                    'position': title.string.replace(","," "),
                    # 'kind': kind.string
                }
                results.append(job_data)           
        return results
