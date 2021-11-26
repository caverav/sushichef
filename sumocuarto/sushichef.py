#!/usr/bin/env python3
from ricecooker.chefs import SushiChef
from ricecooker.classes.nodes import ChannelNode, HTML5AppNode, SlideshowNode, TopicNode, VideoNode, DocumentNode, AudioNode
from ricecooker.classes.files import DocumentFile, SlideImageFile, ThumbnailFile, VideoFile, AudioFile
from le_utils.constants import licenses
from ricecooker.classes.licenses import get_license

# imports y asignaciones previas respecto al xml
from pytube import YouTube
import re
import requests
from xml.etree import ElementTree as ET
r = requests.get("https://www.curriculumnacional.cl/estudiante/621/xml-article-239671.xml")
root = ET.fromstring(r.content)

class MineducChef(SushiChef):

    channel_info = {
        'CHANNEL_SOURCE_DOMAIN': 'curriculumnacional.cl',
        'CHANNEL_SOURCE_ID': 'sumo4tobasico',
        'CHANNEL_TITLE': 'Sumo 4° Básico',
        'CHANNEL_LANGUAGE': 'es',
        'CHANNEL_THUMBNAIL': 'https://www.curriculumnacional.cl/estudiante/621/articles-239671_imagen_portada.thumb_iCuadrada.jpg',
        'CHANNEL_DESCRIPTION': 'Programa educativo del Gobierno de Chile',
     }

    def construct_channel(self, *args, **kwargs):
        channel = self.get_channel(*args, **kwargs)

        topicos = ["Textos escolares oficiales 2021"]
        topico_index = 0
        semana_aux = "Semana 0"
        semanas = []
        c=0
        for child in root: # itera por cada hijo del xml
            topico = TopicNode(source_id="topic"+str(topico_index), title=topicos[topico_index])
            channel.add_child(topico)
            topico_index += 1
            for cchild in child: # itera por cada artículo
                c+=1
                # extrae el titlo y el link del recurso a partir de los atributos <name> y <link>
                titulo = cchild.find("name").text
                if child.attrib['bid'] == '9480':#textos [pdf]
                    recurso = cchild.findall("./binaries/binary[@id='textoescolar_descarga']/link")[0].text
                    thumb = cchild.findall("./binaries/binary[@id='textoescolar_descarga']/thumb_link")[0].text
                    document_file = DocumentFile(path=recurso)
                    examplepdf = DocumentNode(thumbnail=thumb,title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))
                    topico.add_child(examplepdf)

                if child.attrib['bid'] == '9478': #clases [pdf]
                    if cchild.findall("./binaries/binary[@id='recurso_pdf']/link") != []:
                        recurso = cchild.findall("./binaries/binary[@id='recurso_pdf']/link")[0].text
                        thumb =  cchild.findall("./binaries/binary[@id='recurso_pdf']/thumb_link")[0].text
                    else:
                        recurso = cchild.findall("./binaries/binary[@id='recurso_1']/link")[0].text
                        thumb =  cchild.findall("./binaries/binary[@id='recurso_1']/thumb_link")[0].text

                    document_file = DocumentFile(path=recurso)
                    examplepdf = DocumentNode(thumbnail=thumb, title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))
                    semana_pdf = cchild.findall("./properties/property[@pnid='823']/property-value[@pnid='823']")[0].text

                    if semana_pdf != semana_aux:
                        semana = TopicNode(source_id=semana_pdf, title=semana_pdf)
                        semana_aux = semana_pdf
                        topico.add_child(semana)
                        semana.add_child(examplepdf)
                    else:
                        semana.add_child(examplepdf)

                if child.attrib['bid'] == '9481': #lecturas [pdf]
                    recurso = cchild.findall("./binaries/binary[@id='recurso_pdf']/link")[0].text
                    thumb = cchild.findall("./binaries/binary[@id='recurso_pdf']/thumb_link")[0].text
                    document_file = DocumentFile(path=recurso)
                    examplepdf = DocumentNode(thumbnail=thumb, title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))
                    topico.add_child(examplepdf)

                if child.attrib['bid'] == '9479': # audiolibros [mp3]
                    recurso = cchild.findall("./binaries/binary[@id='recurso_mp3']/link")[0].text
                    if cchild.findall("./binaries/binary[@id='imagen_portada']/thumb_link") != []:
                        thumb = cchild.findall("./binaries/binary[@id='imagen_portada']/thumb_link")[0].text
                    else:
                        thumb = cchild.findall("./binaries/binary[@id='thumbnail']/thumb_link")[0].text
                    document_file = AudioFile(path=recurso)
                    examplepdf = AudioNode(thumbnail=thumb, title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))
                    topico.add_child(examplepdf)

                if child.attrib['bid'] == '9482': # orientaciones [mp4]
                    recurso = "://www.curriculumnacional.cl/offline/videos/descargas/" + YouTube(cchild.findall("./binaries/binary[@id='youtube']/url")[0].text).video_id + ".mp4"
                    thumb = cchild.findall("./binaries/binary[@id='youtube']/thumb_link")[0].text
                    document_file = VideoFile(path=recurso)
                    examplepdf = VideoNode(thumbnail=thumb, title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))
                    topico.add_child(examplepdf)
        return channel


if __name__ == '__main__':
    chef = MineducChef()
    chef.main()
