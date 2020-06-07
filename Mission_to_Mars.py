from bs4 import BeautifulSoup
import requests
import pprint
from splinter import Browser
import time 
import pandas as pd

# define an overal function
def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    title,paragraph = marsNew(browser)
    data={"title": title,
         "paragraph": paragraph,
         "feature_image": featuredImg(browser),
         "weather": marsWeather(browser),
         "fact": marsFacts(browser),
        #  "hemisphere": hemisphere(browser)
    }

    browser.quit()
    return data

# define function for latest headline
def marsNew(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Extract article title and paragraph text

    try: 
        title = soup.find("div", class_='list_text')
        title1 = title.find("div", class_="content_title").text
        titlePara = title.find("div", class_ ="article_teaser_body").text
    except AttributeError:
        return None, None
    return title1,titlePara

#define a function for featured images
def featuredImg(browser):
    featured_image_url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)

    #Access the webpage
    hImage = browser.html
    soup = BeautifulSoup(hImage, 'html.parser')
    img = soup.find('article').find('a').get("data-fancybox-href")

    imgUrl = 'https://jpl.nasa.gov' + img
    return imgUrl 

# define a function for Mars weather
def marsWeather(browser):
    url2 = 'https://twitter.com/marswxreport?lang=ensol'
    browser.visit(url2)
    time.sleep(1) # https://stackoverflow.com/questions/15866426/beautifulsoup-not-grabbing-dynamic-content
    html2 = browser.html
    soup = BeautifulSoup(html2, 'html.parser')

    marTweet = soup.findAll("span", {'class':'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'})
    #print(marTweet)

    for tweet in marTweet:
        if "InSight sol" in tweet.text and "low" in tweet.text:
            marsWeather = tweet.text
            print(marsWeather)
            break

# define a function for Mars facts
def marsFacts(browser):
    factUrl = "https://space-facts.com/mars/"
    marFacts = pd.read_html(factUrl)
    marDf = marFacts[0]
    marDf.columns = ['Category', 'Data']
    htmlTable = marDf.to_html(classes="table table-striped")
    return htmlTable

# define a function for Mars hemispheres
def hemisphere(browser):
    url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url3)

    html3 = browser.html
    soup = BeautifulSoup(html3,"html.parser")
    marHem = soup.find_all('div', class_= 'item')
    base_url = "https://astrogeology.usgs.gov"
    resultList = []

    # for loop to go through four hemispheres
    for hem in marHem:
        title = hem.find('div', class_='description').find('h3').text
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        imageHem = hem.find('a', class_='itemLink product-item')['href']
        url=base_url+ imageHem
        hemiSum={}
        hemiSum['title']=title
        hemiSum['url']=url
        resultList.append(hemiSum)
        browser.visit(url3)
        time.sleep(1)
    return resultList