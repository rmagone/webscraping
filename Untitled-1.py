from selenium.webdriver.firefox.options import Options
<<<<<<< HEAD
import time
from features.helpers.sql_helper import fetch_db_data, store_data_in_table
from features.helpers.email_helper import send_email
=======
import sqlalchemy
import time

parser = argparse.ArgumentParser()
parser.add_argument("string")

args = parser.parse_args()
print(args.string)
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
>>>>>>> d60b32e4a18b85bf2e297c960954304dcd8db305
options = Options()
options.headless = False
try:
<<<<<<< HEAD
    driver = webdriver.Firefox(
        executable_path="/home/nan/Downloads/AutomationOnPython/geckodriver", options=options)
=======
    driver = webdriver.Firefox(executable_path="/home/nan/webscraping/geckodriver",options=options)
>>>>>>> d60b32e4a18b85bf2e297c960954304dcd8db305
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
    time.sleep(6)
    driver.find_element_by_css_selector(
<<<<<<< HEAD
        ".css-47sehv").click() if args.string == "dzirkstele" else ""

    vol = []
=======
        "button[aria-label='PIEKRĪTU']").click() if args.string == "dzirkstele" else ""
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
    receiver_email = "kristina.kravale@gmail.com"  # Enter receiver address
    password = "Gladiator1992"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily report from: "+args.string
    message["From"] = sender_email
    message["To"] = receiver_email
    text = ""
>>>>>>> d60b32e4a18b85bf2e297c960954304dcd8db305
    for element in elem:
        print('-------------------------')
        data = fetch_db_data("table name")
        if len(data) < 1:
            store_data_in_table(data, element, elem2, elem2, "")
            vol.append("<HTML><BODY> <p>"+element.text + "</p><p> " + elem2[elem.index(
                element)].text + "</p><p> "+element.get_attribute("href") + "</p><br></BODY></HTML>")
        else:
            print("no need to save, already exists")
        print('-------------------------')
    if len(vol) > 0:
        send_email("",vol)

finally:
    driver.close()
