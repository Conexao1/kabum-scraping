import time
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrap import WebScraping
from typing import Type
from os import makedirs

class KabumProduct():
    def __init__(self, product) -> None:
        try:
            self.productName = product.find_element(By.CSS_SELECTOR, "span.nameCard").text
            self.productPrice = product.find_element(By.CSS_SELECTOR, "span.priceCard").text.split()[1]
            self.productLink = product.find_element(By.CSS_SELECTOR, "a.productLink").get_attribute("href")
        except Exception as e:
            print(f"Find Error: {e}")
            self.productName = "N/A"
            self.productPrice = "N/A"
            self.productLink = "N/A"

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
        pageCont = 1
        try:
            lastPage =  int(driver.find_elements(By.CSS_SELECTOR, "a.page")[-1].text)
        except:
            lastPage = 1
        while pageCont <= lastPage:
            print(f"On {pageCont} page.")
            linkPage = f"{self.link}?page_number={pageCont}&page_size=20&facet_filters=&sort=most_searched"
            driver.get(linkPage)
            time.sleep(5)
            allProducts =  driver.find_elements(By.CSS_SELECTOR, "article.productCard")

            for product in allProducts:
                self.addProduct(KabumProduct(product))

            pageCont += 1
        driver.quit()

    def addProduct(self, product: Type[KabumProduct]) -> None:
        self.productsList.append(product)
        
    def writeOutput(self, outputName: str) -> None:
        nameList = [product.productName for product in self.productsList]
        priceList = [product.productPrice for product in self.productsList]
        linkList = [product.productLink for product in self.productsList]
        
        makedirs("./outputs", exist_ok=True)
        df = pandas.DataFrame({"Name": nameList, "Price(R$)": priceList, "Link": linkList})
        df.to_csv(f"./outputs/kabum_{outputName}.csv", encoding='utf-8', sep=';')
        df.to_excel(f"./outputs/kabum_{outputName}.xlsx", engine='xlsxwriter')
