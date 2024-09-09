import time
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrap import WebScraping
from typing import Type, List
from os import makedirs

class AmazonProduct:
    def __init__(self, product) -> None:
        try:
            self.productName = product.find_element(By.CSS_SELECTOR, "span.a-color-base.a-text-normal").text
            self.productPrice = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
            self.productLink = product.find_element(By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href")
        except Exception as e:
            print(f"Find Error: {e}")
            self.productName = "N/A"
            self.productPrice = "N/A"
            self.productLink = "N/A"

#class AmazonScrap(WebScraping):
class AmazonScrap(WebScraping):
    def __init__(self, link) -> None:
        self.productsList: List[AmazonProduct] = []
        self.link = link

    def setup(self) -> webdriver.Chrome:
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        driver = webdriver.Chrome(options = chromeOptions)
        return driver
    
    def getProducts(self) -> None:
        driver =  self.setup()
        driver.get(self.link)
        time.sleep(5)

        pageCont = 1
        while True:
            print(f"On {pageCont} page.")
            time.sleep(2)
            allProducts =  driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")

            for product in allProducts:
                #print(product)
                self.addProduct(AmazonProduct(product))
            try:
                nextPageButton = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
                if(nextPageButton.get_attribute("aria-disabled") == "true"):
                    print("No more pages")
                    break
                nextPageButton.click()
                time.sleep(5)
            except Exception as e:
                print(f"Error during scraping: {e}")
                break

            pageCont += 1

        driver.quit()

    def addProduct(self, product: Type[AmazonProduct]) -> None:
        self.productsList.append(product)

    def writeOutput(self, outputName: str) -> None:
        nameList = [product.productName for product in self.productsList]
        priceList = [product.productPrice for product in self.productsList]
        linkList = [product.productLink for product in self.productsList]
        
        makedirs("./outputs", exist_ok=True)
        df = pandas.DataFrame({"Name": nameList, "Price(R$)": priceList, "Link": linkList})
        df.to_csv(f"./outputs/amazon_{outputName}.csv", encoding='utf-8', sep=';')
        df.to_excel(f"./outputs/amazon_{outputName}.xlsx", engine='xlsxwriter')
