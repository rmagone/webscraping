from selenium.webdriver.firefox.options import Options
import time
from features.helpers.sql_helper import fetch_db_data, store_data_in_table
from features.helpers.email_helper import send_email
options = Options()
options.headless = False
try:
    driver = webdriver.Firefox(
        executable_path="/home/nan/Downloads/AutomationOnPython/geckodriver", options=options)
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
        ".css-47sehv").click() if args.string == "dzirkstele" else ""

    vol = []
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
