#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import os



def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser =  Browser('chrome', **executable_path, headless=False)

    # In[3]:


    #URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)


    # In[4]:


    html = browser.html
    soup = bs(html, 'html.parser')


    # In[5]:


    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print(news_p)


    # In[6]:


    #URL of page to be scraped
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    # In[7]:


    browser.links.find_by_partial_text('FULL').click()


    # In[8]:


    # Parse 
    html = browser.html
    soup = bs(html, 'html.parser')


    # In[9]:


    partial_image_url = soup.find('img', class_='fancybox-image').get('src')
    print(partial_image_url)


    # In[10]:


    print(url)


    # In[11]:


    #Save complete url string for this image
    featured_image_url = url + partial_image_url
    print(featured_image_url)


    # In[12]:


    #URL of page to be scraped
    url = 'https://galaxyfacts-mars.com/'
    
    #browser.visit(url)


    # In[13]:


    tables = pd.read_html(url)
    print(tables)


    # In[14]:


    type(tables)


    # In[15]:


    mars_df = tables[1]
    mars_df


    # In[16]:


    mars_df.columns=["Facts", "Mars"]
    mars_df.set_index("Facts")
    mars_df


    # In[17]:


    #Use Pandas to convert the data to a HTML table string
    html_table = mars_df.to_html(buf=None)

    # In[18]:


    #URL of page to be scraped
    url = 'https://marshemispheres.com/'
    browser.visit(url)


    # In[19]:


    # Parse 
    html = browser.html
    soup = bs(html, 'html.parser')

    hemispheres = soup.find_all(class_='item')


    # In[20]:


    partial_url = 'https://marshemispheres.com/'
    hemisphere_image_urls = []

    for x in hemispheres:
        title = x.find('h3').text
        full_img_url = partial_url + x.find('a')['href']
        response = requests.get(full_img_url)
        soup = bs(response.text, 'html.parser')
        img_url = soup.find('ul').li.a['href']
        hem_dict = {'title': title, 'img_url': partial_url + img_url}
        hemisphere_image_urls.append(hem_dict)
        
        


    # In[21]:


    print(hemisphere_image_urls)


    # In[22]:


    browser.quit()

    scraped_data = { 
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'html_table': html_table,
        'hemisphere_image_urls': hemisphere_image_urls

    }

    return scraped_data

