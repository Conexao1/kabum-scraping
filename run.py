from scrap import KabumScrap

link = str(input("URL: "))
output = str(input("File name output: "))

kabum = KabumScrap(link)
kabum.getProducts()
kabum.writeOutput(output)
