from xml.etree import ElementTree as ET
import requests
url = "https://www.curriculumnacional.cl/estudiante/621/xml-article-239657.xml"
r = requests.get(url)
root = ET.fromstring(r.content)
# iterate over root
for child in root:
    for cchild in child:
        print("TITULO: " + cchild.find("name").text) #TITULO
        print("\tLINK: "+ cchild.find("binaries").find("binary").find("link").text)
        print()
