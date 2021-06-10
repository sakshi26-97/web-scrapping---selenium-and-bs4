from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import re
from get_all_data import get_all_content_from_page

def trade_spider(driver, url_list, url_dictionary, text_list, text_dictionary):
    blacklist = []
    

    """
    Selenium hands the page source to Beautiful Soup
    """
    soup = BeautifulSoup(driver.page_source, 'lxml')
   
    """
    Beautiful Soup grabs all anchor tag and split into href and text of the current page
    """

    for link in soup.findAll('a'):
        url = link.get('href')
        text = " ".join(re.findall("[a-zA-Z]+", link.getText()))

        if not url.startswith('https'):
            url = '<base-url>'+url
            if url not in blacklist:
                if url not in url_list:
                    url_list.append(url)
                    text_list.append(json.dumps(text)[1:len(json.dumps(text))-1])

    url_dictionary['home'] = url_list
    text_dictionary['home'] = text_list

    explore_each_url(driver,url_list, url_dictionary, text_list, text_dictionary,blacklist)


def explore_each_url(driver, url_list, url_dictionary, text_list, text_dictionary, blacklist):
    try:
        name = ''
        keys = url_dictionary.keys() 
        for key in keys:
            for index in range(len(url_dictionary[key])): 
                len_url_list = len(url_list)
                """
                Explores page given by the URL
                """
                driver.get(url_dictionary[key][index])
            
                soup = BeautifulSoup(driver.page_source,'lxml')

                for link in soup.findAll('a'):
                    url = link.get('href')
                    print('url',url)
                    text = " ".join(re.findall("[a-zA-Z]+", link.getText()))

                    # if url in ['javascript:void(0);', 'javascript:void(0)', 'javascript://']:
                    #     print('true')
                    #     print('//a[@href="'+url+'"]')
                    #     find_url = driver.find_element_by_xpath('//a[@href="'+url+'"]')
                        # find_url.click()

                    if url != None:
                        if not url.startswith('https'):
                            url = '<base-url>'+url

                            if url not in blacklist:
                                if url not in url_list:
                                    url_list.append(url)
                                    text_list.append(json.dumps(text)[1:len(json.dumps(text))-1])

                                    name = key+'.'+text_dictionary[key][index]

                                    url_dictionary[name] = url_list[len_url_list:len(url_list)-1]
                                    text_dictionary[name] = text_list[len_url_list:len(text_list)-1]
        for key in keys:
            del url_dictionary[key]
            del text_dictionary[key]

        """
        If values of url_dictionary not empty then execute get_all_content_from_page function
        """
        # if bool(url_dictionary):
        #     get_all_content_from_page(driver, url_dictionary) 

        if len(url_dictionary) > 0:
            explore_each_url(driver, url_list, url_dictionary, text_list, text_dictionary, blacklist)

    except Exception as e:
        print('Error occured',e)


        