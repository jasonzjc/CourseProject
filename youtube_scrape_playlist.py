from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re

def webdriver_init():
    '''
    create a webdriver object and set options for headless browsing
    '''
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('./chromedriver',options=options)
    return driver

def get_js_soup(url,driver):
    '''
    get javascript to html, parse it to generate a soup object
    '''
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

def playlist_generation(url):
    '''
    genearte YouTube playlist given the playlist URL
    the output include:
    1. title of each video
    2. URL of each video
    3. Video number of each video
    '''

    driver = webdriver_init()
    soup = get_js_soup(url,driver) 
    playlist = {}
    url_head = 'http://www.youtube.com'
    for a in soup.findAll('a', attrs={'class':'yt-simple-endpoint style-scope ytd-playlist-video-renderer'}):
        video_title = a.get('title')
        video_link = a.get('href')
        video_number = re.search('watch\?v=(.+)&list',video_link).group(1)
        playlist[video_title] = (video_number,url_head+video_link)
    
    return playlist

if __name__ == "__main__":
    url = 'https://www.youtube.com/playlist?list=PLUl4u3cNGP63z5HAguqleEbsICfHgDPaG'
    playlist = playlist_generation(url)
    print(playlist)