from scrap import WebScraping
from typing import Type
import time
import pandas
from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class KabumProduct():
    def __init__(self, product) -> None:
        # self.productName = product.find_element(By.CLASS_NAME, "nameCard").text
        self.productPrice = product.find_element(By.CLASS_NAME, "priceCard").text.split()[1]
        self.productLink = product.find_element(By.CLASS_NAME, "productLink").get_attribute("href")

class KabumScrap(WebScraping):
    def __init__(self, link) -> None:
        self.productsList = []
        self.link = link

    def setup(self) -> webdriver.Chrome:
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")

        driver = webdriver.Chrome(options = chromeOptions)
        return driver

    def getProducts(self) -> None:
        driver =  self.setup()
        driver.get(self.link)

        howManyProducts = driver.find_element(By.ID, "listingCount").text.split()
        howManyProducts = int(howManyProducts[0])

        if(howManyProducts <= 20):
            allProducts =  driver.find_elements(By.CLASS_NAME, "productCard")

            for product in allProducts:
                self.addProduct(KabumProduct(product))
        else:
            lastPage = ceil(howManyProducts/20) + 1

            for page in range(1, lastPage):
                linkPage = f"{self.link}?page_number={page}&page_size=20&facet_filters=&sort=most_searched"
                driver.get(linkPage)
                print(f"On {page} page.")
                time.sleep(3)

                allProducts =  driver.find_elements(By.CLASS_NAME, "productCard")

                for product in allProducts:
                    self.addProduct(KabumProduct(product))
        driver.close()

    def addProduct(self, product: Type[KabumProduct]) -> None:
        self.productsList.append(product)
        
    def writeOutput(self, outputName: str) -> None:
        nameList = [product.productName for product in self.productsList]
        priceList = [product.productPrice for product in self.productsList]
        linkList = [product.productLink for product in self.productsList]
        
        df = pandas.DataFrame({"Name": nameList, "Price(R$)": priceList, "Link": linkList})
        df.to_csv(f"./outputs/kabum_{outputName}.csv", encoding='utf-8', sep=';')
        df.to_excel(f"./outputs/kabum_{outputName}.xlsx", engine='xlsxwriter')
