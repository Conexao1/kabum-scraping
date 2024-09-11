from scrap import KabumScrap, AmazonScrap

link = str(input("URL: "))
output = str(input("File name output: "))

if("kabum" in link.lower()):
    print("Scraping Kabum")
    kabum = KabumScrap(link)
    kabum.getProducts()
    kabum.writeOutput(output)
else:
    print("Scraping Amazon")
    amazon = AmazonScrap(link)
    amazon.getProducts()
    amazon.writeOutput(output)

