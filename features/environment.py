from selenium import webdriver
import os
from configparser import ConfigParser
from selenium.webdriver.common.keys import Keys
import platform
from behave.fixture import use_fixture_by_tag
from selenium.webdriver.firefox.options import Options
import subprocess
from webdriver_manager import firefox
from webdriver_manager.firefox import GeckoDriverManager
import re
import wget
import requests


def before_scenario(context, scenario):
    #response = subprocess.Popen("ps cax | grep cloud_sql_proxy",
    #                            shell=True,
    #                            stdout=subprocess.PIPE,
    #                            )
    #stdout_list = response.communicate()[0]
    #if(len(stdout_list) < 1):
    #    print("content not found")
    #    os.system("/home/nan/go/bin/cloud_sql_proxy -instances=exemplary-proxy-322717:"
    #              + "europe-central2:postcollector=tcp:3306 &")
        #os.system("/home/nan/cloud_sql_proxy -instances=exemplary-proxy-322717:"
         #         + "europe-central2:postcollector=tcp:3306 &")
   # else:
        # print("content found {}".format(str(stdout_list).split('\\n')))
    options = Options()
    options.headless = True

    if platform.machine().endswith("armv7l"):
        context.browser = webdriver.Firefox(
            executable_path= manageArmDriverDownload(), options=options)
    else:
          #      context.browser = webdriver.Firefox(
         #   executable_path= manageArmDriverDownload(), options=options)
        context.browser = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(), options=options)

def after_scenario(context, scenario):
    context.browser.close()


def manageArmDriverDownload():
    # get firefox version
    firefox_version = str(subprocess.Popen("firefox --version",
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           ).communicate()[0])
    print(firefox_version)
    # get and check if such file vversion found
    print("ls | grep "+re.search("\d\d", firefox_version).group()+"")
    files_found = str(subprocess.Popen("ls |grep "+re.search("\d\d", firefox_version).group()+"",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       ).communicate()[0])
    if len(files_found) < 4:
        response = requests.get(
            "https://launchpad.net/ubuntu/focal/armhf/firefox-geckodriver")
        regex = '\/ubuntu\/focal\/armhf\/firefox-geckodriver\/'+re.search("\d\d", firefox_version).group()+'\S+\d"'
        value = re.search(regex, str(response.text))
        response = requests.get(
            "https://launchpad.net"+str(value.group().strip('"')))
        regexForDownload = 'http\S\S+.deb\"'
        file_path = re.search(
            regexForDownload, response.text).group().strip('"')
        file_path = re.search("f.+", file_path)
        wget.download(re.search(regexForDownload, response.text).group().strip(
           '"'), ".", progressBar)
        # http://launchpadlibrarian.net/556871844/firefox-geckodriver_92.0+build3-0ubuntu0.20.04.1_armhf.deb
        subprocess.Popen("dpkg-deb -x "+file_path.group() + " data",
                         shell=True,
                         stdout=subprocess.PIPE,
                         ).communicate()[0]
        path = subprocess.Popen("readlink -f data/usr/bin/geckodriver",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       ).communicate()[0]
        return path.decode().__str__().strip('\n') 
    else: 
        path = subprocess.Popen("readlink -f data/usr/bin/geckodriver",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       ).communicate()[0]
        return path.decode().__str__().strip('\n')

def progressBar(self, current, total):
    print("Downloading: %d%% [%d / %d] bytes" %
          (current / total * 100, current, total))
