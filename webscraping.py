import time
import pandas
from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

url = str(input("Paste your url: "))
outputName = str(input("Type the name of csv and xlsx files outputs: "))

productsDict = {"Model":[], "Price(R$)":[], "Link":[]}

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

howManyProducts = driver.find_element(By.ID, "listingCount").text.split()
howManyProducts = int(howManyProducts[0])

if(howManyProducts <= 20):
    products =  driver.find_elements(By.CLASS_NAME, "productCard")
    for product in products:
        productName = product.find_element(By.CLASS_NAME, "nameCard").text
        productPrice = product.find_element(By.CLASS_NAME, "priceCard").text.split()[1]
        productLink = product.find_element(By.CLASS_NAME, "productLink").get_attribute("href")
        productsDict["Model"].append(productName)
        productsDict["Price(R$)"].append(productPrice)
        productsDict["Link"].append(productLink)
else:
    lastPage = ceil(howManyProducts/20)

    for page in range(1, lastPage + 1):
        urlPage = f"{url}?page_number={page}&page_size=20&facet_filters=&sort=most_searched"
        driver.get(urlPage)
        print(f"On {page} page.")
        time.sleep(3)
        products =  driver.find_elements(By.CLASS_NAME, "productCard")
        for product in products:
            productName = product.find_element(By.CLASS_NAME, "nameCard").text
            productPrice = product.find_element(By.CLASS_NAME, "priceCard").text.split()[1]
            productLink = product.find_element(By.CLASS_NAME, "productLink").get_attribute("href")
            productsDict["Model"].append(productName)
            productsDict["Price(R$)"].append(productPrice)
            productsDict["Link"].append(productLink)

driver.close()

df = pandas.DataFrame(productsDict)

df.to_csv(f"./{outputName}.csv", encoding='utf-8', sep=';')
df.to_excel(f"./{outputName}.xlsx", engine='xlsxwriter')