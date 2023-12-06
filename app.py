from flask import Flask, render_template, request, redirect, url_for,flash,jsonify,session
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc


app = Flask(__name__)
app.secret_key = 'secret_key'



def ebayURL(search):
    URL = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw='+'+'.join(search.split())
    return URL


def firstColumn(ebayURL,search,driver):
    #Buy it now, used, Low to High
    driver.get(ebayURL)
    buyItNowURL = driver.find_element('xpath','//*[@id="mainContent"]/div[1]/div/div[2]/div[2]/div[1]/div/ul/li[3]/a').get_attribute('href')
    driver.get(buyItNowURL)
    
    try:
        liNum = None
        ele = driver.find_element('xpath','/html/body/div[4]/div[4]/div[1]/div/div[2]/div[2]/div[2]/span[1]/span/ul')
        soup = BeautifulSoup(ele.get_attribute('innerHTML'), 'html.parser')
        for num,i in enumerate(soup.find_all('li')):
            if i.find(string='Used') == 'Used':
                liNum = num+1
        if liNum != None:
            usedURL = driver.find_element('xpath',f'/html/body/div[4]/div[4]/div[1]/div/div[2]/div[2]/div[2]/span[1]/span/ul/li[{liNum}]/a').get_attribute('href')
            driver.get(usedURL)
        else:
            pass
    except:
        print(f'Exception in usedURL')
        pass
    
    try:
        liNum = None
        ele = driver.find_element('xpath', '/html/body/div[4]/div[4]/div[1]/div/div[2]/div[3]/div[1]/div/span/span/ul')
        soup = BeautifulSoup(ele.get_attribute('innerHTML'), 'html.parser')
        for num,i in enumerate(soup.find_all('li')):
            if i.find(string='Price + Shipping: lowest first') == 'Price + Shipping: lowest first':
                liNum = num+1
        if liNum != None:
            lowPriceURL = driver.find_element('xpath', f'/html/body/div[4]/div[4]/div[1]/div/div[2]/div[3]/div[1]/div/span/span/ul/li[{liNum}]/a').get_attribute('href')
            driver.get(lowPriceURL)
        else:
            pass
    except:
        print(f'Exception in lowPriceURL')
        pass
    
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    productPriceTag = soup.find('ul', class_='srp-results srp-list clearfix').find('span', class_='s-item__price')
    if productPriceTag is not None:
        productPrice = productPriceTag.text
        heading = soup.find_all('div', class_='s-item__title')[1].find('span', role='heading').text
        if search.split()[-1] not in heading:
            productPrice = None
    else:
        productPrice = None
        
    return productPrice


def secondColumn(ebayURL,search,driver):
    #Buy it now, Sold Item, used, High to low
    driver.get(ebayURL)
    try:
        buyItNowURL = driver.find_element('xpath','//*[@id="mainContent"]/div[1]/div/div[2]/div[2]/div[1]/div/ul/li[3]/a').get_attribute('href')
        driver.get(buyItNowURL)
    except:
        print(f'Exception in buyItNowURL')
        pass
    
    try:  
        soldItemURL = driver.find_element('xpath','//li[@name="LH_Sold"]/div/a').get_attribute('href')
        driver.get(soldItemURL.replace('&LH_Complete=1',''))
    except:
        print('Exception in soldItemURL')
        pass
    
    try:
        liNum = None
        ele = driver.find_element('xpath','/html/body/div[4]/div[4]/div[1]/div/div[2]/div[2]/div[2]/span[1]/span/ul')
        soup = BeautifulSoup(ele.get_attribute('innerHTML'), 'html.parser')
        for num,i in enumerate(soup.find_all('li')):
            if i.find(string='Used') == 'Used':
                liNum = num+1
        if liNum != None:
            usedURL = driver.find_element('xpath',f'/html/body/div[4]/div[4]/div[1]/div/div[2]/div[2]/div[2]/span[1]/span/ul/li[{liNum}]/a').get_attribute('href')
            driver.get(usedURL)
        else:
            pass
    except:
        print('Exception in usedURL')
        pass
    
    try:
        liNum = None
        ele = driver.find_element('xpath', '/html/body/div[4]/div[4]/div[1]/div/div[2]/div[3]/div[1]/div/span/span/ul')
        soup = BeautifulSoup(ele.get_attribute('innerHTML'), 'html.parser')
        for num,i in enumerate(soup.find_all('li')):
            if i.find(string='Price + Shipping: highest first') == 'Price + Shipping: highest first':
                liNum = num+1
        if liNum != None:
            highToLowURL = driver.find_element('xpath',f'/html/body/div[4]/div[4]/div[1]/div/div[2]/div[3]/div[1]/div/span/span/ul/li[{liNum}]/a').get_attribute('href')
            driver.get(highToLowURL)
        else:
            pass
        
    except:
        print('Exception in highToLowURL')
        pass

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    productPriceTag = soup.find('ul', class_='srp-results srp-list clearfix').find('span', class_='s-item__price')
    if productPriceTag is not None:
        productPrice = productPriceTag.text
        heading = soup.find_all('div', class_='s-item__title')[1].find('span', role='heading').text
        if search.split()[-1] not in heading:
            productPrice = None
    else:
        productPrice = None
    return productPrice


def thirdColumn(ebayURL,search,driver):
    # New, Buy it now, Low to High
    driver.get(ebayURL)
    try:
        liNum = None
        ele = driver.find_element('xpath','/html/body/div[4]/div[4]/div[1]/div/div[2]/div[2]/div[2]/span[1]/span/ul')
        soup = BeautifulSoup(ele.get_attribute('innerHTML'), 'html.parser')
        for num,i in enumerate(soup.find_all('li')):
            if i.find(string='New') == 'New':
                liNum = num+1
        if liNum != None:
            newURL = driver.find_element('xpath', f'/html/body/div[4]/div[4]/div[1]/div/div[2]/div[2]/div[2]/span[1]/span/ul/li[{liNum}]/a').get_attribute('href')
            driver.get(newURL)
        else:
            pass
    except:
        print(f'Exception in newURL')
        pass

    buyItNowURL = driver.find_element('xpath','//*[@id="mainContent"]/div[1]/div/div[2]/div[2]/div[1]/div/ul/li[3]/a').get_attribute('href')
    driver.get(buyItNowURL)
    
    try:
        liNum = None
        ele = driver.find_element('xpath', '/html/body/div[4]/div[4]/div[1]/div/div[2]/div[3]/div[1]/div/span/span/ul')
        soup = BeautifulSoup(ele.get_attribute('innerHTML'), 'html.parser')
        for num,i in enumerate(soup.find_all('li')):
            if i.find(string='Price + Shipping: lowest first') == 'Price + Shipping: lowest first':
                liNum = num+1
        if liNum != None:
            lowPriceURL = driver.find_element('xpath', f'/html/body/div[4]/div[4]/div[1]/div/div[2]/div[3]/div[1]/div/span/span/ul/li[{liNum}]/a').get_attribute('href')
            driver.get(lowPriceURL)
        else:
            pass
    except:
        print(f'Exception in lowPriceURL')
        pass
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    productPriceTag = soup.find('ul', class_='srp-results srp-list clearfix').find('span', class_='s-item__price')
    if productPriceTag is not None:
        productPrice = productPriceTag.text
        heading = soup.find_all('div', class_='s-item__title')[1].find('span', role='heading').text
        if search.split()[-1] not in heading:
            productPrice = None
    else:
        productPrice = None
    return productPrice

def findPrice(modelNumber):
    partSelectURL = 'https://www.partselect.com/Models/{}/'.format(modelNumber)
    response = requests.get(partSelectURL)
    soup = BeautifulSoup(response.content, 'html.parser')
    appliance  = soup.find('h1').text.split(modelNumber)[-1].split()[0]

    searches = []
    partDivElements = soup.find('div', class_='row mt-3 align-items-stretch').find_all('div', class_='col-md-6 mb-3')
    for part in partDivElements:
        modelEle = part.find('div', class_='mb-1')
        manufacturerNum = modelEle.get_text(strip=True).split(':')[-1].strip()
        search = appliance + ' ' + manufacturerNum
        searches.append(search)

    data = []
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options) 
    for search in searches[:2]:
        di = {}
        url = ebayURL(search)

        first = firstColumn(url,search,driver)
        second = secondColumn(url,search,driver)
        third = thirdColumn(url,search,driver)

        di['search'] = search
        di['firstColumn'] = first
        di['secondColumn'] = second
        di['thirdColumn'] = third
        print(di)
        data.append(di)

    driver.quit()
    return data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_number = request.form['modelNumber']
        result_data = findPrice(model_number)
        return render_template('index.html', result=result_data)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run()