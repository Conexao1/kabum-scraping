from scrap import KabumScrap, AmazonScrap

link = str(input("URL: "))
output = str(input("File name output: "))

if("kabum".lower() in link):
    print("kabum")
    kabum = KabumScrap(link)
    kabum.getProducts()
    kabum.writeOutput(output)
else:
    print("amazon")
    amazon = AmazonScrap(link)
    amazon.getProducts()
    amazon.writeOutput(output)
