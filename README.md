# Web Scraping Take Home Assignment

This repo demonstrates the solutions I came up with for the UpWage take home assignment.

### Features

- Connecting to local Postgres jobs table
- Accessing web page specified in the indeed_job_url column
- Scraping job page data based on job expired state
- Updating records in postgresql
- Junction table design
- Sample SQL query for many to many relationship, given job id

<br /><br />

## Part One: Scraper

<br />

### Environment Variables

To run this project, you will need to add the following environment variables to an .env file

`HOST` ,
`DATABASE` ,
`USERNAME` ,
`PW` ,
`PORT`

These are used to establish a connection between the project and a local Postgres database.

<br />

### Packages needed

Install the following python packages with pip3

```bash
  requests
  psycopg2
  beautifulsoup4
  python-dotenv
  lxml
```

The approach used in my code assumes there is an existing jobs table that looks like this (only has indeed_job_url initially)

![Empty DB Screenshot](/images/initial_db.png)

Open up index.py and run with the following command, or press the 'play' button in VS Code in the upper right. You will see some logs in the terminal stating if the job is expired or not.

```bash
python3 index.py
```

![Terminal Logs Screenshot](/images/terminal_logs.png)

<br /><br />

## Part Two: Extra Credit, Encouraged to Complete

<br />

### Junction Table (Many to Many) Design

![DB Screenshot](/images/db.png)

Note: In jobs_attributes, job_id and attribute_id are foreign keys pointing to a record's id in their respective table.

Additional note: the text data type was chosen for descriptions in case arbitrarily long description text needs to be stored. Otherwise, varchar is used for generally shorter string attributes like title, name, category, posted_date, etc

https://dbdiagram.io/d/62dc67c70d66c74655383eef

<br />

### SQL Query

```sql
select *
from jobs_attributes
join jobs on jobs.id = jobs_attributes.job_id
join attributes on attributes.id = jobs_attributes.attribute_id
where jobs.id = YOUR_JOB_ID
```

Example
![SQL Query Screenshot](/images/query_example.png)

<br /><br />

## Part 3: Extra Credit, Optional

One approach I would try is using an AWS lambda that rotates IPs regularly. Lambda functions are not guaranteed to preserve their IP address, which resets every 6 min the lamda is not used. There is also no limit to the number of lambdas you can create with AWS. An additional note, is that this would be cost effective since you only pay for the amount used per lambda, rather than paying for having a server up and running 24/7. To create multiple lambdas we can go through the AWS console or Terraform.

Another approach I would try, to avoid reinventing the wheel, is a rotating proxy service like Zyte Smart Proxy Manager. This is an API where the requests you make would be routed through a pool of high quality proxies.
https://docs.zyte.com/smart-proxy-manager/integrations/python.html
You would need to install zyte-smartproxy-ca.crt in your OS and make sure the python requests library is using version 2.18 or greater.
