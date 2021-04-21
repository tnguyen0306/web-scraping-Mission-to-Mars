import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


def scrape():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    mars_dict = {}
    
    # NASA Mars News
    nasa_url = "https://mars.nasa.gov/news/"
    driver.get(nasa_url)
    time.sleep(3)
    nasa_html = driver.page_source
    nasa_soup = bs(nasa_html, features="html.parser")
    nasa_results = nasa_soup.find(class_="slide")
    news_titles = nasa_results.find("h3").text
    news_p = nasa_results.find(class_="article_teaser_body").text
    mars_dict["news_titles"] = news_titles
    mars_dict["news_p"] = news_p

    # JPL Mars Space Images - Featured Image
    feat_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    driver.get(feat_url)
    time.sleep(3)
    feat_html = driver.page_source
    feat_soup = bs(feat_html)
    feat_results = feat_soup.find("img", class_="headerimage fade-in")['src']
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + feat_results
    mars_dict["featured_image_url"] = featured_image_url

    # Mars Facts
    fact_url = "https://space-facts.com/mars/"
    table = pd.read_html(fact_url)
    table_fact = table[0]
    table_fact.columns = ["Description","Mars"]
    mars_fact = table_fact.to_html(index=False)
    mars_dict["mars_fact"] = mars_fact

    # Mars Hemispheres
    hemisphere_image_urls = []
    hem_url = [
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced",
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    ]

    for u in hem_url:
        driver.get(u)
        time.sleep(3)
        hem_html = driver.page_source
        hem_soup = bs(hem_html)
        hem_title = hem_soup.find("h2", class_="title").text
        hem_title = hem_title.replace(" Enhanced","")
        hem_img = hem_soup.find("div", class_="downloads").find("a")["href"]
        hem_info = {"title": hem_title, "img_url": hem_img}
        hemisphere_image_urls.append(hem_info)

    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_dict

    time.sleep(5)
    driver.close()

if __name__ == "__main__":
    print(scrape())