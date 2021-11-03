#!/usr/bin/env python3
import re
import requests
from xml.etree import ElementTree as ET
r = requests.get("https://www.curriculumnacional.cl/estudiante/621/xml-article-239657.xml")
root = ET.fromstring(r.content)
# iterate over root
for child in root:
    for cchild in child:
        
        print("TITULO: " + cchild.find("name").text) 

        if child.attrib['bid'] == '9480':#textos
            print("\tLink: "+ cchild.findall("./binaries/binary[@id='textoescolar_descarga']/link")[0].text)
            print("\tThumb:: "+ cchild.findall("./binaries/binary[@id='textoescolar_descarga']/thumb_link")[0].text)
        
        if child.attrib['bid'] == '9478': #clases
            print("\tLink: " + cchild.findall("./binaries/binary[@id='recurso_pdf']/link")[0].text)
            print("\tThumb: " + cchild.findall("./binaries/binary[@id='recurso_pdf']/thumb_link")[0].text)
        
        if child.attrib['bid'] == '9481': #lecturas
            print("\tLink: " + cchild.findall("./binaries/binary[@id='recurso_pdf']/link")[0].text)
            print("\tThumb: " + cchild.findall("./binaries/binary[@id='recurso_pdf']/thumb_link")[0].text)

        if child.attrib['bid'] == '9479': # audiolibros
            print("\tLink: " + cchild.findall("./binaries/binary[@id='recurso_mp3']/link")[0].text)
            if cchild.findall("./binaries/binary[@id='imagen_portada']/thumb_link") != []:
                print("\tThumb: " + cchild.findall("./binaries/binary[@id='imagen_portada']/thumb_link")[0].text)
            else:
                print("\tThumb: " + cchild.findall("./binaries/binary[@id='thumbnail']/thumb_link")[0].text)
