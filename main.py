from bs4 import BeautifulSoup
import psycopg2
import requests

host = 'localhost'
database = 'jobs'
username = 'karen'
pwd = ''
port = '5432'
conn = None
cur = None


try:
    conn = psycopg2.connect(
        host = host,
        dbname = database,
        user = username,
        password = pwd,
        port = port
    )
    cur = conn.cursor()

    cur.execute('SELECT * FROM jobs')
    #for record in cur.fetchall():
        #print(record);
        #print('')
        
   
except Exception as error:
    print(error)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

# with open('home.html', 'r') as html_file:
#     content = html_file.read()
#     soup = BeautifulSoup(content, 'lxml')
#     # find() returns first element found
#     #tags = soup.find('h5')
#     course_cards = soup.find_all('div', class_='card')
#     for course in course_cards:
#         course_name = course.h5.text
#         #Note, -1 index lets you grab the last element in array
#         course_price = course.a.text.split()[-1]
       
#         print(f'{course_name} costs {course_price}')
#         print('')
    #print(soup.prettify())

print('Put some skill that you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

def findJobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for job in jobs:
        published_date = job.find('span', class_='sim-posted').span.text
        if 'few' in published_date:
            company_name = job.find('h3', 'joblist-comp-name').text.replace(' ', '')
            skills = job.find('span', class_="srp-skills").text.replace(' ', '')
            more_info = job.header.h2.a['href']
            if unfamiliar_skill not in skills:


                print(f"Company Name: {company_name.strip()}")
                print(f"Required Skills: {skills.strip()}")
                print(f"More Info: {more_info}")

                print("")
