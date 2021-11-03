#!/usr/bin/env python3
import re
import requests
from xml.etree import ElementTree as ET
r = requests.get("https://www.curriculumnacional.cl/estudiante/621/xml-article-239657.xml")
root = ET.fromstring(r.content)

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
