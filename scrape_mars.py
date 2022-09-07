# dependencies and setup
from bs4 import BeautifulSoup as soup
from splinter import Browser
import pandas as me
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    # splinter setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    # mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # setup parse
    html = browser.html
    news = soup(html, 'html.parser')
    # get first title and first teaser paragraph
    news_title = news.find('div', class_='content_title').get_text()
    news_p = news.find('div', class_='article_teaser_body').get_text()

    # jpl site for featured mars image
    img_url = 'https://spaceimages-mars.com'
    browser.visit(img_url)
    # setup parse
    html = browser.html
    img_soup = soup(html, 'html.parser')
    time.sleep(1)
    # find and click the full image button
    full_img = browser.find_by_tag('button')[1]
    full_img.click()
    # find the relative image url and save full url
    rel_img_url = img_soup.find('img', class_='headerimage fade-in').get('src')
    featured_img_url = f'https://spaceimages-mars.com/{rel_img_url}'
    # find and save featured image title
    img_title = img_soup.find('h1', class_='media_feature_title').get_text()

    # mars facts, using pandas to scrape mars facts
    facts_url = 'https://galaxyfacts-mars.com'
    mars_df = me.read_html(facts_url)[1]
    mars_df.columns = ['description', 'value']
    mars_df = mars_df.set_index('description')
    # convert table to html
    mars_table = mars_df.to_html(classes='data table', index=False, header=False, border=1)

    # site for mars hemispheres
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    # setup parse
    html = browser.html
    hemis = soup(html, 'html.parser')
    time.sleep(1)
    # create a list to hold images and titles
    hemi_img_urls = []

    # loop through each image and add to dictionary list
    # results = soup.find_all('div', class_='item')
    for result in range(4):
        # go through each article to get wanted information
        browser.links.find_by_partial_text('Hemisphere')[result].click()
        # parse
        html = browser.html
        hemis = soup(html, 'html.parser')
        # scrape
        title = hemis.find('h2', class_='title').text
        hemi_url = hemis.find('li').a.get('href')
        # store results into a dictionary and append to the list
        hemispheres = {}
        hemispheres['title'] = title
        hemispheres['img_url'] = f'https://marshemispheres.com/{hemi_url}'
        hemi_img_urls.append(hemispheres)

    # crate dictionary to store retrieved data
    mars_info = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image': featured_img_url,
        'mars_facts': mars_table,
        'hemispheres': hemi_img_urls
    }

    # close browser after scraping
    browser.quit()

    # return results
    return mars_info