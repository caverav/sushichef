#!/usr/bin/env python3
import re
import requests
from xml.etree import ElementTree as ET
r = requests.get("https://www.curriculumnacional.cl/estudiante/621/xml-article-239657.xml")
root = ET.fromstring(r.content)
<<<<<<< HEAD
# iterate over root
for child in root:
    for cchild in child:
        
        
        #print()

        if child.attrib['bid'] == '9480':
            print("TITULO: " + cchild.find("name").text) #TITULO

            if cchild.find("binaries").find("binary").attrib['id'] == "textoescolar_descarga":
                print("\tLINK: "+ cchild.find("binaries").find("binary").find("link").text)
                print("\tLINK: "+ cchild.find("binaries").find("binary").find("thumb_link").text)
        

        #print(cchild.find("binaries").find("binary").attrib['id'])
=======

for child in root: # itera por cada hijo del xml
    for cchild in child: # itera por cada artículo

        # extrae el titlo y el link del recurso a partir de los atributos <name> y <link>
        titulo, recurso = cchild.find("name").text, cchild.find("binaries").find("binary").find("link").text

        # imprime de forma legible la estructura de lo extraido
        print("\nTítulo: " + titulo + "\n|") 
        print("|__ Recurso: "+ recurso) 
        # Si no es mp3
        if not (re.search("\.mp3$", recurso)): 
            print("|__ Miniatura: " + cchild.find("binaries").find("binary").find("thumb_link").text + "\n")
        # Si es mp3
        else: 
            print("|__ Miniatura: No tienen miniatura los mp3\n")
>>>>>>> 71b9c0520f498858bdc9abd3a26d00067ff1ee2a
