from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://books.toscrape.com/")

images = []
imageCount = 0
bookName=[]
price=[] 
stockStatus=[] 
rating=[] 
description=[] 
productInformation=[] 
category=[]

for page in range(5):
    WebDriverWait(driver,30).until(
    EC.presence_of_element_located((By.CLASS_NAME,"thumbnail"))
    )
    images=(driver.find_elements(By.CLASS_NAME,"thumbnail"))
    for image in images:
        image.click()
        imageCount+=1
        time.sleep(2)


        rawName=driver.find_element(By.XPATH,"//h1")
        bookName.append(rawName.text)
        rawPrice=driver.find_element(By.CLASS_NAME,"price_color")
        price.append(rawPrice.text)
        rawStockStatus=driver.find_element(By.XPATH,"//*[contains(text(), 'stock')]")
        stockStatus.append(rawStockStatus.text.split("(")[0])
        rawRating=driver.find_element(By.CLASS_NAME,"star-rating")
        rawRating = rawRating.get_attribute("class").split()[1]
        rating.append(rawRating)
        rawDescription=driver.find_elements(By.TAG_NAME,"p")[3]
        description.append(rawDescription.text)
        rawInformation=driver.find_elements(By.TAG_NAME,"tr")
        infoBlock=[]
        for info in rawInformation:
            infoBlock.append(info.text)
        productInformation.append(infoBlock)
        rawCategory=driver.find_element(By.CLASS_NAME,"breadcrumb").find_elements(By.TAG_NAME,"li")[2]
        print(rawCategory.text)
        category.append(rawCategory.text)


        driver.back()

        if imageCount == 20:
            imageCount = 0
            break

    WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"next"))
    )
    next=driver.find_element(By.PARTIAL_LINK_TEXT,"next")
    next.click()

    print(len(bookName))
    print(len(price))
    print(len(stockStatus))
    print(len(rating))
    print(len(description))
    print(len(productInformation))
    print(len(category))

df = pd.DataFrame({"Bookname":bookName,"Price":price,"Stock status":stockStatus,"Rating":rating,"Description":description,"Product information":productInformation,"Category":category})
df.to_csv("All Products data.csv",line_terminator='\n\n')
print(df)

driver.quit()


