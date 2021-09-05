from selenium import webdriver
import os
from configparser import ConfigParser
from selenium.webdriver.common.keys import Keys
import time
from behave.fixture import use_fixture_by_tag
from selenium.webdriver.firefox.options import Options
import subprocess

def before_scenario(context, scenario):
    response = subprocess.Popen("ps cax | grep cloud_sql_proxy",
                             shell=True,
                             stdout=subprocess.PIPE,
                           )
    stdout_list = response.communicate()[0]
    print(len(stdout_list))
    if(len(stdout_list)<1):
        print("content not found")
        os.system("/home/nan/cloud_sql_proxy -instances=exemplary-proxy-322717:"
        + "europe-central2:postcollector=tcp:3306 &")
    else:
        print("content found {}".format(str(stdout_list).split('\\n')))
    options = Options()
    options.headless = False
    context.browser = webdriver.Firefox(
        executable_path="/home/nan/PycharmProjects/webscraper/geckodriver", options=options)


def after_scenario(context, scenario):
    context.browser.close()
