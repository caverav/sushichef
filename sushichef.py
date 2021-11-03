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
r = requests.get("https://www.curriculumnacional.cl/estudiante/621/xml-article-239657.xml")
root = ET.fromstring(r.content)

class MineducChef(SushiChef):
    """
    The SushiChef class takes care of uploading channel to Kolibri Studio.
    """

    # 1. PROVIDE CHANNEL INFO  (replace <placeholders> with your own values)
    ############################################################################
    channel_info = {
        'CHANNEL_SOURCE_DOMAIN': 'curriculumnacional.cl',       # who is providing the content (e.g. learningequality.org)
        'CHANNEL_SOURCE_ID': 'pruebas',                   # channel's unique id
        'CHANNEL_TITLE': 'Prueba',
        'CHANNEL_LANGUAGE': 'es',
        # 'CHANNEL_THUMBNAIL': 'http://yourdomain.org/img/logo.jpg', # (optional) local path or url to image file
        'CHANNEL_DESCRIPTION': 'What is this channel about?',      # (optional) description of the channel (optional)
     }

    # 2. CONSTRUCT CHANNEL
    ############################################################################
    def construct_channel(self, *args, **kwargs):
        """
        This method is reponsible for creating a `ChannelNode` object and
        populating it with `TopicNode` and `ContentNode` children.
        """
        # Create channel
        ########################################################################
        channel = self.get_channel(*args, **kwargs)     # uses self.channel_info

        c=0
        for child in root: # itera por cada hijo del xml
            for cchild in child: # itera por cada artículo
                c+=1
                # extrae el titlo y el link del recurso a partir de los atributos <name> y <link>

                titulo = cchild.find("name").text
                #TODO: falta poner thumbnails
                if child.attrib['bid'] == '9480':#textos [pdf]
                    recurso = cchild.findall("./binaries/binary[@id='textoescolar_descarga']/link")[0].text
                    thumb = cchild.findall("./binaries/binary[@id='textoescolar_descarga']/thumb_link")[0].text
                    document_file = DocumentFile(path=recurso)
                    examplepdf = DocumentNode(title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))
                
                if child.attrib['bid'] == '9478': #clases [pdf]
                    recurso = cchild.findall("./binaries/binary[@id='recurso_pdf']/link")[0].text
                    thumb =  cchild.findall("./binaries/binary[@id='recurso_pdf']/thumb_link")[0].text
                    document_file = DocumentFile(path=recurso)
                    examplepdf = DocumentNode(title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))
                
                if child.attrib['bid'] == '9481': #lecturas [pdf]
                    recurso = cchild.findall("./binaries/binary[@id='recurso_pdf']/link")[0].text
                    thumb = cchild.findall("./binaries/binary[@id='recurso_pdf']/thumb_link")[0].text
                    document_file = DocumentFile(path=recurso)
                    examplepdf = DocumentNode(title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))

                if child.attrib['bid'] == '9479': # audiolibros [mp3]
                    recurso = cchild.findall("./binaries/binary[@id='recurso_mp3']/link")[0].text
                    if cchild.findall("./binaries/binary[@id='imagen_portada']/thumb_link") != []:
                        thumb = cchild.findall("./binaries/binary[@id='imagen_portada']/thumb_link")[0].text
                    else:
                        thumb = cchild.findall("./binaries/binary[@id='thumbnail']/thumb_link")[0].text
                    document_file = AudioFile(path=recurso)
                    examplepdf = AudioNode(title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))

                if child.attrib['bid'] == '9482': # orientaciones [mp4]
                    recurso = "https://www.curriculumnacional.cl/offline/videos/descargas/" + YouTube(cchild.findall("./binaries/binary[@id='youtube']/url")[0].text).video_id + ".mp4"
                    thumb = cchild.findall("./binaries/binary[@id='youtube']/thumb_link")[0].text
                    document_file = VideoFile(path=recurso)
                    examplepdf = VideoNode(title=titulo, source_id=str(c), files=[document_file], license=get_license(licenses.PUBLIC_DOMAIN))


                # Create topics to add to your channel
                ########################################################################
                # Here we are creating a topic named 'Example Topic'
                # exampletopic = TopicNode(source_id=titulo, title=titulo)
                # TODO: Create your topic here

                # Now we are adding 'Example Topic' to our channel
                # channel.add_child(exampletopic)
                # TODO: Add your topic to channel here

                # You can also add subtopics to topics
                # Here we are creating a subtopic named 'Example Subtopic'
                # examplesubtopic = TopicNode(source_id="topic-1a", title="Example Subtopic")
                # TODO: Create your subtopic here

                # Now we are adding 'Example Subtopic' to our 'Example Topic'
                # exampletopic.add_child(examplesubtopic)
                # TODO: Add your subtopic to your topic here


                # Content
                # You can add documents (pdfs and ePubs), videos, audios, and other content
                ########################################################################
                # let's create a document file called 'Example PDF'
                # TODO: Create your pdf file here (use any url to a .pdf file)

                # We are also going to add a video file called 'Example Video'
                # video_file = VideoFile(path="https://ia600209.us.archive.org/27/items/RiceChef/Rice Chef.mp4")
                # fancy_license = get_license(licenses.SPECIAL_PERMISSIONS, description='Special license for ricecooker fans only.', copyright_holder='The chef video makers')
                # examplevideo = VideoNode(title="Example Video", source_id="example-video", files=[video_file], license=fancy_license)
                # TODO: Create your video file here (use any url to a .mp4 file)

                # Finally, we are creating an audio file called 'Example Audio'
                # audio_file = AudioFile(path="https://ia802508.us.archive.org/5/items/testmp3testfile/mpthreetest.mp3")
                # exampleaudio = AudioNode(title="Example Audio", source_id="example-audio", files=[audio_file], license=get_license(licenses.PUBLIC_DOMAIN))
                # TODO: Create your audio file here (use any url to a .mp3 file)

                # Now that we have our files, let's add them to our channel
                channel.add_child(examplepdf) # Adding 'Example PDF' to your channel
                #exampletopic.add_child(examplevideo) # Adding 'Example Video' to 'Example Topic'
                #examplesubtopic.add_child(exampleaudio) # Adding 'Example Audio' to 'Example Subtopic'

                # TODO: Add your pdf file to your channel
                # TODO: Add your video file to your topic
                # TODO: Add your audio file to your subtopic

                # the `construct_channel` method returns a ChannelNode that will be
                # processed by the ricecooker framework
        return channel


if __name__ == '__main__':
    """
    This code will run when the sushi chef is called from the command line.
    """
    chef = MineducChef()
    chef.main()
