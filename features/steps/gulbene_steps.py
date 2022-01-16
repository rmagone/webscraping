import time
from behave import *
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from features.page.gulbene_page import getTitle, getDescription, cookieAgreement
from features.helpers.email_helper import send_email
from features.helpers.sql_helper import store_data_in_table, fetch_db_data


@given(u'launch "{page}" page')
def launch_gulbene_page(context, page):
    print(context)
    if page == "dzirkstele":
        link = "https://dzirkstele.lv/category/vietejas-zinas/"
    else:
        link = "https://www."+page+".lv/lv/"
    print(link)
    context.webpage = page
    context.browser.get(link)


@when('I read data')
def read_page_data(context):
    if context.webpage == "dzirkstele":
        i=0
        print("before a while")
        while i>10 :
            print("I am here")
            print(cookieAgreement(context).is_displayed())
            if cookieAgreement(context).is_displayed():
                cookieAgreement(context).click()
            time.sleep(2)
            i+=1
        print("done")
        print(context.browser.page_source)
        time.sleep(10)
    elem = getTitle(context, context.webpage)
    elem2 = getDescription(context, context.webpage)
    data_to_send = []
    data_to_store = []
    for element in elem:
        print('-------------------------')
        print(element.text)
        print(elem2[elem.index(element)].text)
        val = (element.text, elem2[elem.index(element)].text)
        data = fetch_db_data(context.webpage, val, context)
        if len(data) < 1:
            data_to_send.append("<HTML><BODY> <p>"+element.text + "</p><p> " + elem2[elem.index(
                element)].text + "</p><p> "+element.get_attribute("href") + "</p><br></BODY></HTML>")
            data_to_store.append(val)
        else:
            print("no need to save, already exists")
        print('-------------------------')
    context.data_to_send = data_to_send
    context.data_to_store = data_to_store


@when('store data')
def store_data(context):
    if len(context.data_to_store) > 1:
        store_data_in_table(context.webpage, context.data_to_store, context)
    else:
        print("nothing to send")


@when('send email')
def send_emails(context):
    if len(context.data_to_send) > 0:
        send_email(context.webpage, context.data_to_send,context)
    else:
        print("nothing to send")
