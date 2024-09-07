from abc import ABC, abstractmethod
from selenium import webdriver

class WebScraping(ABC):

    @abstractmethod
    def setup() ->  webdriver.Chrome:
        pass

    @abstractmethod
    def getProducts() -> None:
        pass

    @abstractmethod
    def addProduct() -> None:
        pass

    @abstractmethod
    def writeOutput() -> None:
        pass
