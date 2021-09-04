from selenium import webdriver
import os
from configparser import ConfigParser
from selenium.webdriver.common.keys import Keys
import time
from behave.fixture import use_fixture_by_tag
from selenium.webdriver.firefox.options import Options


def before_scenario(context, scenario):
    options = Options()
    options.headless = False
    context.browser = webdriver.Firefox(
        executable_path="/home/nan/PycharmProjects/webscraper/geckodriver", options=options)


def after_scenario(context, scenario):
    context.browser.close()
