import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


# def scrape_info():
#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     return_data = {}
#     driver.close()
#     return return_data

def scrape():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # NASA Mars News
    nasa_url = "https://mars.nasa.gov/news/"
    driver.get(nasa_url)
    time.sleep(3)
    nasa_html = driver.page_source
    nasa_soup = bs(nasa_html)
    nasa_results = nasa_soup.find(class_="slide")
    news_titles = nasa_results.find("h3").text
    news_p = nasa_results.find(class_="article_teaser_body").text

    # JPL Mars Space Images - Featured Image
    feat_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    driver.get(feat_url)
    time.sleep(3)
    feat_html = driver.page_source
    feat_soup = bs(feat_html)
    feat_results = feat_soup.find("img", class_="headerimage fade-in")['src']
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + feat_results

    # Mars Facts
    fact_url = "https://space-facts.com/mars/"
    table = pd.read_html(fact_url)
    table_fact = table[0]
    table_fact.columns = ["Description","Mars"]
    mars_fact = table_fact.to_html(index=False)

    # Mars Hemispheres
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},   
    ]

    
    driver.close()

if __name__ == "__main__":
    print(scrape_info() )