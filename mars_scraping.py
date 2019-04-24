# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd 
import time
import datetime


# Define executable path
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# Create empty dictionary 
mars_info_dict=dict()



#define URL
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')


slide_elem = news_soup.select_one('ul.item_list li.slide')




slide_elem.find("div", class_='content_title')




news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# Paragraph teaser
news_para = slide_elem.find('div', class_="article_teaser_body").get_text()
news_para



from pprint import pprint
mars_info_dict["Mars_news_title"] = news_title
mars_info_dict["Mars_news_body"] = news_para
pprint(mars_info_dict)


# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.


# ## JPL Mars Space Images - Featured Image



# URL 2 - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url2)



# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# Make sure to find the image url to the full size .jpg image.
# Make sure to save a complete url string for this image.


full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()



html2 = browser.html
img_soup = BeautifulSoup(html2, 'html.parser')




#print (image_soup)




img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel




img_url_final = f'https://www.jpl.nasa.gov{img_url_rel}'




img_url_final



#append into dict

mars_info_dict["Mars_featured_image_url"] = img_url_final
mars_info_dict


# ## Mars Weather



urltwt = 'https://twitter.com/marswxreport?lang=en'
browser.visit(urltwt)
htmltwt = browser.html
souptwt = BeautifulSoup(htmltwt, 'html.parser')


# Scrape the latest Mars weather tweet from the page. 
# Save the tweet text for the weather report as a variable called mars_weather.



mars_weather = souptwt.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
mars_weather



mars_info_dict["Mars_Twitter_Weather"] = mars_weather


# ## Mars Facts



# Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# Use Pandas to convert the data to a HTML table string.




url3 = "http://space-facts.com/mars/"
df_marsfacts_all = pd.read_html(url3)
df_marsfacts = df_marsfacts_all[0]
# df_marsfacts




#change column names
df_marsfacts.columns = ['Mars Facts', 'Values']



df_marsfacts


df_marsfacts.to_html("mars_facts.html", index=False)
#set index for better retrieval
df_marsfacts.set_index("Mars Facts")




mars_facts_html = df_marsfacts.to_html(classes="mars_facts table table-striped")
mars_info_dict["Mars_facts_table"] = mars_facts_html


# ## Mars Hemispheres


# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.




url4 =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url4)
time.sleep(10)
html4 = browser.html
soup4 = BeautifulSoup(html4, "html.parser")




#parse soup object for images
class_collap_results = soup4.find('div', class_="collapsible results")
hemis_items = class_collap_results.find_all('div',class_='item')



# click through the images

hemis_img_urls_list=list()
img_urls_list = list()
title_list = list()
for h in hemis_items:
    #save title
    h_title = h.h3.text
    title_list.append(h_title)
    
    # find the href link.
    h_href  = "https://astrogeology.usgs.gov" + h.find('a',class_='itemLink product-item')['href']
    
    #print(h_title,h_href)
    
    #browse the link from each page
    browser.visit(h_href)
    time.sleep(5)
    #Retrieve the  image links and store in a list. 
    html4   = browser.html
    soup_img = BeautifulSoup(html4, 'html.parser')
    h_img_url = soup_img.find('div', class_='downloads').find('li').a['href']
    print("h_img_url" + h_img_url)
    img_urls_list.append(h_img_url)
    
    # create a dictionary with  each image and title and append to a list. 
    hemispheres_dict = dict()
    hemispheres_dict['title'] = h_title
    hemispheres_dict['img_url'] = h_img_url
    
    hemis_img_urls_list.append(hemispheres_dict)
    
print(hemis_img_urls_list)
print(title_list)
print(img_urls_list)


#add to the dictionary
mars_info_dict["Hemisphere_image_urls"] = hemis_img_urls_list




cur_datetime = datetime.datetime.utcnow()
mars_info_dict["Date_time"] = cur_datetime




pprint(mars_info_dict)





