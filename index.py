import os
import traceback
import requests
import psycopg2
from bs4 import BeautifulSoup
from datetime import date
from dotenv import load_dotenv


# load environment vars
load_dotenv()

# setting up connection and cursor
conn = None
cur = None



def scrapeIndeedJobs():
    try:
        # establish connection and cursor
        conn = psycopg2.connect(
            host = os.getenv('HOST'),
            dbname = os.getenv('DATABASE'),
            user = os.getenv('USERNAME'),
            password = os.getenv('PW'),
            port = os.getenv('PORT')
        )
        cur = conn.cursor()

        cur.execute('SELECT * FROM jobs')
        records = cur.fetchall()

        for record in records:

            indeed_job_url = record[5]
            html_text = requests.get(indeed_job_url).text
            soup = BeautifulSoup(html_text, 'lxml')
            expired_job_header = soup.find('div', class_='jobsearch-JobInfoHeader-expiredHeader')
            today = date.today().strftime("%m/%d/%Y")

            if expired_job_header == None:
                print(f'{record[5]} is not expired. Scraping... ')

                job_title = soup.find('div', class_='jobsearch-JobInfoHeader-title-container').h1.text.replace("'", "")
                job_description = soup.find('div', class_='jobsearch-jobDescriptionText').text.replace("'", "")
                posted_date = soup.find('span', class_='jobsearch-HiringInsights-entry--text').text
                
                update_script = (f"UPDATE jobs SET title = '{job_title}', job_description = '{job_description}', posted_date = '{posted_date}' WHERE id = {record[0]}")
                cur.execute(update_script)

            else:
                print(f"{record[5]} is expired! Updating expired_date to '{today}'")

                update_script = (f"UPDATE jobs SET expired_date = '{today}' WHERE id = {record[0]}")
                cur.execute(update_script)

        conn.commit()
            
    
    except Exception as error:

        # using this to provide more context to the error
        traceback.print_exc()

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


scrapeIndeedJobs()


