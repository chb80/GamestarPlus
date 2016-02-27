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
import urllib, re, time, xbmcaddon
from ui import *;

class GameproWeb(object):
  def __init__(self, gui, loginHandler):    
    self.gui = gui;
    self.loginHandler = loginHandler;
    self.loginDone = "";
    
    self.rootLink = "http://www.gamepro.de";
    self.shortName = "GP";
    
    ##setup regular expressions
    self.imageRegex = "<img src=\".*\" width=\"\\d*\" height=\"\\d*\" alt=\".*\" />"
    self.linkRegex =  "/.*?,\\d*?\\.html"




    self.hrefRegex = "<a (class=\".*?\" ){0,1}href=\""+self.linkRegex+"\" .+?>"
    self.headerRegex ="<strong>.+?</strong>\\s*.*\\s*</a>"
    self.titleRegex = "<a.*?>(.*?)</a>"
    self.simpleLinkRegex = "<a href=\""+self.linkRegex+"\" .+?>.+?</a>";


    self._regEx_extractVideoThumbnail = re.compile("<div class=\"videoPreview\">\\s*"+self.hrefRegex+"\\s*"+self.imageRegex+"\\s*</a>\\s*<span>\\s*"+self.hrefRegex+"\\s*"+self.headerRegex);
    self._regEx_extractTargetLink = re.compile(self.linkRegex);
    self._regEx_extractVideoID = re.compile(",(\\d+)\\.html");
    self._regEx_extractVideoLink = re.compile("http.*(mp4|flv)");
    self._regEx_extractPictureLink = re.compile("//.*.jpg");
    self._regEx_extractHeader = re.compile(self.headerRegex);
    self._regEx_extractSimpleLink = re.compile(self.simpleLinkRegex);
    self._regEx_extractTitle = re.compile(self.titleRegex);
    ##end setup
    
    linkRoot = self.rootLink + "/templates/gamepro/videos/portal/getChannelOverview.cfm";
    imageRoot = "";

    ##setup categories
    self.categories = {
      20001:GalleryObject(linkRoot+"?channelName=search","","","search",True),
      
      30001:GalleryObject(linkRoot+"?channelName=latest&channelMaster=0","","","",True),
      
      30070:GalleryObject(linkRoot+"?channelName=popular&channelMaster=0","","","",True),
      30071:GalleryObject(linkRoot+"?channelName=comments&channelMaster=0","","","",True),
      
      30002:GalleryObject(linkRoot+"?channelId=17&channelMaster=0","","","",True),
      30003:GalleryObject(linkRoot+"?channelId=18&channelMaster=0","","","",True),
      30004:GalleryObject(linkRoot+"?channelId=20&channelMaster=0","","","",True),
      #30005
      30006:GalleryObject(linkRoot+"?channelId=22&channelMaster=0","","","",True),
      30007:GalleryObject(linkRoot+"?channelId=15&channelMaster=0","","","",True),
      30008:GalleryObject(linkRoot+"?channelId=37&channelMaster=0","","","",True),
      30009:GalleryObject(linkRoot+"?channelId=32&channelMaster=0","","","",True),
      30010:GalleryObject(linkRoot+"?channelId=2&channelMaster=0","","","",True),
      30011:GalleryObject(linkRoot+"?channelId=3&channelMaster=0","","","",True),
      
      #30080
      30081:GalleryObject(linkRoot+"?channelId=96&channelMaster=0","","","",True),
      30082:GalleryObject(linkRoot+"?channelId=100&channelMaster=0","","","",True),
      30083:GalleryObject(linkRoot+"?channelId=97&channelMaster=0","","","",True),
      #30084
      30085:GalleryObject(linkRoot+"?channelId=23&channelMaster=0","","","",True),
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
      for videoThumbnail in self._regEx_extractVideoThumbnail.finditer(rootDocument):
        
        videoThumbnail = videoThumbnail.group()
        videoID = self._regEx_extractVideoID.search(videoThumbnail).group(1);
        
        header = self._regEx_extractHeader.search(videoThumbnail).group();
        header = re.sub("(<strong>)|(</strong>)|(</a>)", "", header);
        header = re.sub("\\s+", " ", header);
                
        try:  
          videoObjects.append(self.loadVideoPage(header, videoID));
        except:
          pass;
    return {'videoObjects':videoObjects, 'executed':executed, 'newpage':page+1, 'newpagetext':newpagetext }


  def loadVideoPage(self, title, videoID):
    self.gui.log(self.rootLink+"/emb/getVideoData.cfm?vid="+videoID);
    configDoc = self.loadPage(self.rootLink+"/emb/getVideoData.cfm?vid="+videoID);
    videoLink = unicode(self._regEx_extractVideoLink.search(configDoc).group());
    videoLink = self.replaceXmlEntities(videoLink);
    thumbnailLink =unicode(self._regEx_extractPictureLink.search(configDoc).group());
    
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
