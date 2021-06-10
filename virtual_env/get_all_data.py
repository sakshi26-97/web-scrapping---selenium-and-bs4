from bs4 import BeautifulSoup
import urllib
from selenium import webdriver
from bs4 import BeautifulSoup
import os

def get_all_content_from_page(driver, url_dictionary):
    try:
        type_of_file = ['pdf','docx']
        for key in url_dictionary:
            if len(url_dictionary[key]) != 0:
                folder_name = key.split('.')
                file_name = folder_name[-1]
                folder_name.pop()
                folder_name= '/'.join(folder_name)
                directory = os.getcwd()+'/'+folder_name+'/'

                if not os.path.exists(directory):
                    os.makedirs(directory)
                os.chdir(directory)

                for index in range(len(url_dictionary[key])):
                    if url_dictionary[key][index].find('html') != -1:
                        print('true')
                        extract_html_files(driver, soup, url_dictionary[key][index], file_name)
                   
                    driver.get(url_dictionary[key][index])
                    soup = BeautifulSoup(driver.page_source,'lxml')

                    extract_data(driver, soup, file_name)  

                    extract_img(driver, soup)  

                    extract_video(driver, soup) 

                    for type in type_of_file:
                        extract_files(driver, soup, url_dictionary[key][index], file_name, type)

                os.chdir('/home/sakshi/Desktop/selllenium_webcrawler/virtual_env')

    except Exception as e:
        print('Not found',e)

def extract_data(driver, soup, file_name):
    """
    Extract text content and stores in  folder
    """
    try:
        with open(file_name+'.txt','at') as f:
            for each_data in soup.findAll('p'):
                text = each_data.getText()
                f.write(text.encode('utf8').strip())
        
    except Exception as e:
        print('file not found',e)


def extract_img(driver, soup):
    """
    Download images in images/ folder
    """
    try:
        img_blacklist = ['[[_src]]','[[_imageUrl]]']

        for each_img in soup.findAll('img'):
            if each_img['src'] not in img_blacklist:
                if not each_img['src'].startswith('https'):
                    each_img['src'] = '<base-url>'+each_img['src']
                urllib.urlretrieve(each_img['src'],each_img['alt']+'.png')
    except Exception as e:
        print('Error in extracting image',e)

def extract_video(driver, soup):
    try:
        for each_video in soup.findAll('video'):
            file_name = each_video['title']
            for video_src in each_video.findAll('source'):
                if not video_src['src'].startswith('https'):
                    video_src['src'] = '<base-url>'+video_src['src']
                urllib.urlretrieve(video_src['src'],file_name+'.mp4')
    except Exception as e:
        print('Error in extracting video',e)



def extract_files(driver, soup, url, file_name, type):
    """
    Download html or PDF files
    """
    try:
        if url.endswith(type):
            urllib.urlretrieve(url, file_name+'.'+type)
    except Exception as e:
        print('Error in extracting files',e)

