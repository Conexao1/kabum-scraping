import time
import pandas
from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Products:
    def __init__(self) -> None:
        self.productsList = []

    def addProduct(self, product) -> None:
        self.productName = product.find_element(By.CLASS_NAME, "nameCard").text
        self.productPrice = product.find_element(By.CLASS_NAME, "priceCard").text.split()[1]
        self.productLink = product.find_element(By.CLASS_NAME, "productLink").get_attribute("href")

        self.productsList.append({"productName": self.productName, "productPrice": self.productPrice, "productLink": self.productLink})
        
    def writeOutput(self, outputName: str) -> None:
        nameList = [product["productName"] for product in self.productsList]
        priceList = [product["productPrice"] for product in self.productsList]
        linkList = [product["productLink"] for product in self.productsList]
        
        df = pandas.DataFrame({"Name": nameList, "Price(R$)": priceList, "Link": linkList})
        df.to_csv(f"./{outputName}.csv", encoding='utf-8', sep=';')
        df.to_excel(f"./{outputName}.xlsx", engine='xlsxwriter')
        
products = Products()

url = str(input("Paste your url: "))
outputName = str(input("Type the name of csv and xlsx files outputs: "))

chromeOptions = Options()
chromeOptions.add_argument("--headless")

driver = webdriver.Chrome(options = chromeOptions)
driver.get(url)

howManyProducts = driver.find_element(By.ID, "listingCount").text.split()
howManyProducts = int(howManyProducts[0])

if(howManyProducts <= 20):
    allProducts =  driver.find_elements(By.CLASS_NAME, "productCard")

    for product in allProducts:
        products.addProduct(product)
else:
    lastPage = ceil(howManyProducts/20)

    for page in range(1, lastPage + 1):
        urlPage = f"{url}?page_number={page}&page_size=20&facet_filters=&sort=most_searched"
        driver.get(urlPage)
        print(f"On {page} page.")
        time.sleep(3)
        allProducts =  driver.find_elements(By.CLASS_NAME, "productCard")

        for product in allProducts:
            products.addProduct(product)
       
driver.close()

products.writeOutput(outputName)