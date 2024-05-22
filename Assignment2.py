from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from countries import countries
import pandas as pd
import time


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://quotes.toscrape.com/")

name=[]
nationality=[] 
description=[]
dateOfBirth=[]

for page in range(2):

    WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Next "))
    )
    next=driver.find_element(By.PARTIAL_LINK_TEXT,"Next ")

    aboutLinks = driver.find_elements(By.PARTIAL_LINK_TEXT,"(about)")
    for link in aboutLinks:
        link.click()

        time.sleep(1)
        rawName = driver.find_element(By.CLASS_NAME,"author-title")
        name.append(rawName.text)
        rawNationality=driver.find_element(By.CLASS_NAME,"author-born-location")
        rawNationality = str(rawNationality.text.split(",")[-1])
        if rawNationality[:2]=="in":
            rawNationality = rawNationality.replace("in", "", 1)
        nationality.append(rawNationality)
        rawDescription = driver.find_element(By.CLASS_NAME,"author-description")
        description.append(rawDescription.text)
        rawDateOfBirth = driver.find_element(By.CLASS_NAME,"author-born-date")
        dateOfBirth.append(rawDateOfBirth.text)

        driver.back()

    next.click()

df=pd.DataFrame({"Name":name,"Nationality":nationality,"Description":description,"Date of Birth":dateOfBirth})
df.to_csv("Authors.csv",line_terminator='\n\n')
driver.quit()


