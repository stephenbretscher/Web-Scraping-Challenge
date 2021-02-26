import pandas as pd
from bs4 import BeautifulSoup as bs 
from splinter import Browser
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

#Function to execute all scraping code and return one python dictionary
def scrape_mars_function():

    scraped_data={}


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Visits nasa news webpage for mars
    url_news = "https://mars.nasa.gov/news/"

    browser.visit(url_news)

    #Scrape news site for News Title and Paragraph Text
    html_news = browser.html
    soup = bs(html_news, "html.parser")
    #article allows new 
    article = soup.find("div", class_='list_text')


    #Titles contained in <div class="content_title"
    scraped_data["title"] = article.find("div", class_ = "content_title").text


    #Pragraph text contained in <div class="article_teaser_body"
    scraped_data["paragraph"] = article.find("div", class_ = "article_teaser_body").text

    print("Checkpoint 1")

    #JPL space images
    url_spaceimage = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_spaceimage)

    img_html = browser.html
    img_soup = bs(img_html, "html.parser")

    # Find image url to the full size
    scraped_data["featured_image"] = img_soup.find("img", class_="BaseImage object-contain")["data-src"]
    
    print("Checkpoint 2")

    #Visits the Mars Facts webpage
    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit(url_mars_facts)

    mars_facts = pd.read_html(url_mars_facts)
    mars_facts
    mars_facts_df = mars_facts[0]

    mars_facts_df.columns = ["Fact", "Value"]

    #sets index to fact column 
    mars_facts_df.set_index("Fact", inplace=True)

    mars_facts_df

    #save table to html
    mars_facts_df.to_html("mars_facts_data.html")

    print("Checkpoint 3")

    #Mars Hemispheres
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    #HTML object
    html_hemisphere = browser.html
    soup = bs(html_hemisphere, "html.parser")

    # Scrape all items that contain mars hemispheres information
    hemispheres = soup.find_all("div", class_="item")

    # empty dictionary to be appended
    mars_hemispheres = []
    hemispheres_url = "https://astrogeology.usgs.gov"

    # Loop through the list of all hemispheres information
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        hemispheres_img = hemisphere.find("a", class_="itemLink product-item")["href"]
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_url + hemispheres_img)
        
        # HTML Object
        image_html = browser.html
        image_info = bs(image_html, "html.parser")
        
        # Create full image url
        hemisphere_url = hemispheres_url + image_info.find("img", class_="wide-image")["src"]
        
        mars_hemispheres.append({"title" : title, "img_url" : hemisphere_url})

    #print title + url
        print(title)
        print(hemisphere_url)

    print("Checkpoint 4")
    
    scraped_data["mars_hemispheres"] = mars_hemispheres

    print (scraped_data)
        
    return scraped_data

scrape_mars_function()


