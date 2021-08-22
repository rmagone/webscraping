from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import ssl
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import argparse
import datetime
import logging
import os
from selenium.webdriver.firefox.options import Options
import sqlalchemy


parser = argparse.ArgumentParser()
parser.add_argument("string")

args = parser.parse_args()
print(args.string)
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
options = Options()
options.headless=True
try:
    driver = webdriver.Firefox(executable_path="/home/nan/webscraping/firefox",options=options)
    link = "https://dzirkstele.lv/vietejas-zinas/visas-zinas" if args.string == "dzirkstele" else "https://www.gulbene.lv/lv/"
    print(link)
    driver.get(link)
    valueToAssert = "Vietējās ziņas" if args.string == "dzirkstele" else "Gulbenes novads - Sākums"
    print(valueToAssert)
    print(driver.title)
    assert (valueToAssert in driver.title)
    elem = driver.find_elements_by_css_selector(
        ".news.articles .namelink" if args.string == "dzirkstele" else "h2 a[itemprop='url']")
    elem2 = driver.find_elements_by_css_selector(
        ".news.articles .intro" if args.string == "dzirkstele" else "div[itemprop='blogPost']")
    driver.find_element_by_css_selector(
        ".css-47sehv").click() if args.string == "dzirkstele" else ""
    vol = []
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
   # cloud_sql_connection_name = os.environ["exemplary-proxy-322717:europe-central2:postcollector"]
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username="misterdummy",  # e.g. "my-database-user"
            password="1234",  # e.g. "my-database-password"
            database='postcollector',  # e.g. "my-database-name"
            host="127.0.0.1",
            port="3306"
        ),
    )
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "mwslatvia@gmail.com"  # Enter your address
    receiver_email = "rmagone@gmail.com"  # Enter receiver address
    password = "Gladiator1992"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily report from: "+args.string
    message["From"] = sender_email
    message["To"] = receiver_email
    text = ""
    for element in elem:
        print('-------------------------')
        sql_select_Query = "select * from "+args.string + \
            " where name = %s and context = %s order by id desc limit 1"
        val = (element.text, elem2[elem.index(element)].text)
        with pool.connect() as conn:
            # Execute the query and fetch all results
            records = conn.execute(
                sql_select_Query,val
            ).fetchall()
        # get all records
        print("Total number of rows in table: ", len(records))
        if len(records) < 1:
            sql = "INSERT INTO "+args.string+" (name, context) VALUES (%s, %s)"
            print(sql)
            with pool.connect() as conn:
                conn.execute(sql,val)
                print("record inserted.")
            vol.append("<HTML><BODY> <p>"+element.text + "</p><p> " + elem2[elem.index(
                element)].text + "</p><p> "+element.get_attribute("href") + "</p><br></BODY></HTML>")
        else:
            print("no need to save, already exists")
        print('-------------------------')
    message.attach(MIMEText(text.join(vol), 'html', 'utf-8'))
    if len(vol) > 0:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()   # optional
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        # ...send emails
except smtplib.SMTPException as e:
    print('Something went wrong...'+e)
finally:
    driver.close()
