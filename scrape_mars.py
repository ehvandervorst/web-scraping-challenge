#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import time
import pandas as pd

#Open Chrome Driver browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

#Collect latest news from NASA Mars news site

def scrape():
    mars_dict = {}
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news'
    browser.visit(news_url)
    time.sleep(3)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    slides = news_soup.find_all("li", class_="slide")
    news_title = slides[0].find("div", class_="content_title").text
    news_paragraph = slides[0].find("div", class_="article_teaser_body").text

#JPL Mars Featured Image
    base_url = "https://www.jpl.nasa.gov"
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    time.sleep(3)
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')
    image = jpl_soup.find_all('img')[3]["src"]
    image_url = base_url + image

#Mars facts
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    facts_df = tables[0]
    facts_df.columns = ['Description', 'Value']
    facts_html = facts_df.to_html()

#Mars Hemisphere images
    usgs_url = 'https://astrogeology.usgs.gov'
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemi_url)
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')
    mars_hemispheres = hemi_soup.find('div', class_='collapsible results')
    all_hemispheres = mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []

    for i in all_hemispheres:
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text

        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)
        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(image_dict)

#Create dictionary of scraped info
    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": image_url,
        "mars_facts": facts_html,
        "hemisphere_images": hemisphere_image_urls
    }

    browser.quit()
    return mars_dict