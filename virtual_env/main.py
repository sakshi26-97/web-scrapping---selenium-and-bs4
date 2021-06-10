from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import yaml
from crawl import trade_spider
import time


def get_config():
    """
    Reads configurations from the config.yaml file and returns a dictionary
    """
    with open('./config.yaml','r') as config_file:
        configuration = yaml.load(config_file, Loader=yaml.FullLoader)
    return configuration

def init():
    global config
    global driver
    global url_dictionary
    global url_list
    global text_list
    global text_dictionary
    is_initialized = False
    try:
        config = get_config()
        chrome_options = Options()
        """
        Creates new instance of Chrome in Incognito mode
        """
        chrome_options.add_argument("--incognito") 
        chrome_options.add_argument("download.default_directory=/home/sakshi/Desktop/crawl_content") 
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/home/sakshi/Desktop/selllenium_webcrawler/virtual_env/chromedriver_linux64/chromedriver')
        driver.maximize_window()
        url = config['URL']
        """
        Explores page given by the URL
        """
        driver.get(url)
        url_dictionary = {}
        text_dictionary = {}
        url_list = ['<url1>','<url2>']
        text_list = ['PV002: Roles, Responsibilities, and Relationships of Early Childhood Professionals - PV002','PV001: History and Evolution of the Early Childhood Field - PV001']
        is_initialized = True

    except FileNotFoundError as file_not_found_error:
        print("Error: File Not Found", file_not_found_error)

    except Exception as e:
        print("Exception occured", e)
        
    finally:
        return is_initialized


def login():
    """
    Fetch username, password input boxes and login button
    """
    
    # username = driver.find_element_by_id('userNameInput')
    # password = driver.find_element_by_id('passwordInput')
    # login = driver.find_elements_by_xpath('//form/div/div/span[@class = "submit"]')

    username = driver.find_element_by_id('userName')
    password = driver.find_element_by_id('password')
    login = driver.find_elements_by_xpath('//form/div/button[@class = "d2l-button"]')

    """
    Input text in username and password input boxes
    """

    username.send_keys(config['USERNAME'])
    password.send_keys(config['PASSWORD'])
    # driver.find_element_by_id('userNameInput').clear()
    # username.send_keys(config['USERNAME'])
    """
    Click on the "login" button
    """
    login[0].click()
    
    trade_spider(driver, url_list, url_dictionary, text_list, text_dictionary)


if __name__ == '__main__':  
    if init():
        login()
    else:
        print("Failed to connect")