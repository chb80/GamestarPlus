# -*- coding: utf-8 -*-
#-------------LicenseHeader--------------
# plugin.video.chb80_gamestar - Downloads/view videos from gamepro.de
# Copyright (C) 2015  chb80 [chb80@gmx.de]
# based on GamestarVideo [plugin.video.gamestar] 0.1.5 Copyright (C) 2010  Raptor 2101 [raptor2101@gmx.de]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 
import urllib, re, time, xbmcaddon, traceback
from ui import *;

class GameproWeb(object):
  def __init__(self, gui, loginHandler):    
    self.gui = gui;
    self.loginHandler = loginHandler;
    self.loginDone = "";
    
    self.rootLink = "http://www.gamepro.de/";
    self.shortName = "GP";
    
    ##setup regular expressions
    self._regEx_extractVideoID = re.compile("/videos/.*,(\\d*)\\.html");
    self._regEx_extractVideoLink = re.compile("http.*(mp4|flv)");
    self._regEx_extractPictureLink = re.compile("(http://|//).*.jpg");
    self._regEx_extractTitle = re.compile("<videoname>\\d*?\\.(.*)\\.embed</videoname>");
    ##end setup
    
    linkRoot = self.rootLink+"videos/video-kanaele/";
    imageRoot = "http://images.gamestar.de/images/idgwpgsgp/bdb/";   

    ##setup categories
    self.categories = {
#      20001:GalleryObject(linkRoot+"?channelName=search","","","search",True),
      
      30001:GalleryObject(linkRoot+"alle-videos,9100,newest/", imageRoot+"2018270/b144x81.jpg","","",True),
      
      ######30070:GalleryObject(linkRoot+"?channelName=popular&channelMaster=0","","","",True),
      ######30071:GalleryObject(linkRoot+"?channelName=comments&channelMaster=0","","","",True),
      
      30002:GalleryObject(linkRoot+"tests,17/",imageRoot+"2018272/b144x81.jpg","","",True),
      30003:GalleryObject(linkRoot+"previews,18/",imageRoot+"2018269/b144x81.jpg","","",True),
      30004:GalleryObject(linkRoot+"specials,20/",imageRoot+"2018270/b144x81.jpg","","",True),
      #30005
      ######30006:GalleryObject(linkRoot+"?channelId=22&channelMaster=0","","","",True),
      ######30007:GalleryObject(linkRoot+"?channelId=15&channelMaster=0","","","",True),
      ######30008:GalleryObject(linkRoot+"?channelId=37&channelMaster=0","","","",True),
      30009:GalleryObject(linkRoot+"technik-checks,32/","2557236/b144x81.jpg","","",True),
      30010:GalleryObject(linkRoot+"boxenstop,2/",imageRoot+"2018274/b144x81.jpg","","",True),
      30011:GalleryObject(linkRoot+"trailer,3/","2017073/b144x81.jpg","","",True),
      
      30080:GalleryObject(linkRoot+"frisch-gestrichen,104/",imageRoot+"2645072/b144x81.jpg","","",True),
      30081:GalleryObject(linkRoot+"was-ist-,96/",imageRoot+"2018270/b144x81.jpg","","",True),
      30082:GalleryObject(linkRoot+"news,100/",imageRoot+"2764165/b144x81.jpg","","",True),
      30083:GalleryObject(linkRoot+"gamewatch,97/",imageRoot+"2018270/b144x81.jpg","","",True),
      30084:GalleryObject(linkRoot+"monats-vorschau,24/",imageRoot+"2757586/b144x81.jpg","","",True),      
      ######30085:GalleryObject(linkRoot+"?channelId=23&channelMaster=0","","","",True),
      #30086
      
      
      }
      
    import xml.dom.minidom
    linksXML = xml.dom.minidom.parse(urllib.urlopen("http://chb80.spdns.org/binaries/show_dynbin.php4?dynbin_id=PLUGIN_VIDEO_CHB80_GAMESTAR_LINKS_GP"))
    for mainNode in linksXML.childNodes:
      if mainNode.nodeName == "links":
        for linkNode in mainNode.childNodes:
          if linkNode.nodeName == "link":
            id = int(linkNode.getAttribute("id")) + 9100000
            for attributeNode in linkNode.childNodes:
              if attributeNode.nodeName == "link":
                link = attributeNode.firstChild.data.strip()
              elif attributeNode.nodeName == "imagelink":
                imagelink = "" #attributeNode.firstChild.data.strip()
              elif attributeNode.nodeName == "title":
                title = attributeNode.firstChild.data.strip()
            if(link.startswith('http://')):
              self.categories[id]=GalleryObject(link, imageRoot+imagelink,title,"",True);
            elif(link.startswith('https://')):
              self.categories[id]=GalleryObject(link, imageRoot+imagelink,title,"",True);
            else:
              self.categories[id]=GalleryObject(linkRoot+link, imageRoot+imagelink,title,"",True);                     
    ##endregion
    
  def getCategories(self):
    categories={};
    for key in self.categories.keys():
      categories[key]=self.categories[key];
    return categories;
  
  def getVideoLinkObjects(self, categorieid, page, userstring):
    addon = xbmcaddon.Addon("plugin.video.chb80_gamestar")
  
    videoObjects = [];
    executed = False
    newpagetext = "";
    
    if categorieid in self.categories:
      categorie = self.categories[categorieid];
      executed = True      
      categorie_url = categorie.url;
      if(not categorie.userstring_parameter == ""):
        categorie_url += "&"+categorie.userstring_parameter+"="+userstring;
      categorie_url += "&p=%s"%page;
      self.gui.log(categorie_url);
      rootDocument = self.loadPage(categorie_url);
            
      videoIds = set();
      for match in self._regEx_extractVideoID.finditer(rootDocument):       
        videoId = match.group(1);
        if(videoId not in videoIds):
          videoIds.add(videoId);
          
      for videoId in sorted(videoIds, reverse=True):        
        try:
          videoObjects.append(self.loadVideoPage(videoId));
        except:
          self.gui.log("something goes wrong while processing "+videoId);
          self.gui.log("Exception: ");
          traceback.print_exc();
          self.gui.log("Stacktrace: ");
          traceback.print_stack();
    return {'videoObjects':videoObjects, 'executed':executed, 'newpage':page+1, 'newpagetext':newpagetext }


  def loadVideoPage(self, videoID):
    self.gui.log(self.rootLink+"/emb/getVideoData.cfm?vid="+videoID);
    configDoc = self.loadPage(self.rootLink+"/emb/getVideoData.cfm?vid="+videoID).decode('utf-8');
    videoLink = self._regEx_extractVideoLink.search(configDoc).group();
    videoLink = self.replaceXmlEntities(videoLink);
    thumbnailLink = self._regEx_extractPictureLink.search(configDoc).group();
    title = self._regEx_extractTitle.search(configDoc).group(1);
    title = self.transformHtmlCodes(title);
    
    if(not thumbnailLink.startswith('http://')):
      thumbnailLink = thumbnailLink.replace("//",'http://');
    thumbnailLink = thumbnailLink;
    
    return VideoObject(title, videoLink, "http:"+thumbnailLink, self.shortName);
  
  def replaceXmlEntities(self, link):
    entities = (
        ("%3A",":"),("%2F","/"),("%3D","="),("%3F","?"),("%26","&")
      );
    for entity in entities:
       link = link.replace(entity[0],entity[1]);
    return link;
  def transformHtmlCodes(self,string):
    replacements = (
      (u'Ä', u'&Auml;'),
      (u'Ü', u'&Uuml;'),
      (u'Ö', u'&Ouml;'),
      (u'ä', u'&auml;'),
      (u'ü', u'&uuml;'),
      (u'ö', u'&ouml;'),
      (u'ß', u'&szlig;'),
      (u'\"',u'&#034;'),
      (u'\"',u'&quot;'),
      (u'\'',u'&#039;'),
      (u'&', u'&amp;'),
      (u' ', u'&nbsp;')
    )
    for replacement in replacements:
      string = string.replace(replacement[1],replacement[0]);
    return string;
  def loadPage(self,url):
    try:
      safe_url = url.replace( " ", "%20" ).replace("&amp;","&")
      sock = urllib.urlopen( safe_url )
      doc = sock.read()
      if doc:
        return doc
      else:
        return ''
    except:
      return ''
