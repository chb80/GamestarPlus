# -*- coding: utf-8 -*-
#-------------LicenseHeader--------------
# plugin.video.chb80_gamestar - Downloads/view videos from gamestar.de
# Copyright (C) 2015  chb80 [chb80@gmx.de]
# based on GamestarVideo [plugin.video.gamestar] 0.1.8 Copyright (C) 2010  Raptor 2101 [raptor2101@gmx.de]
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
import urllib, re, time,traceback, xbmcgui, mechanize, xbmcaddon;
from ui import *;

class GamestarWeb(object):
  def __init__(self, gui, loginHandler, plus_user):        
    self.gui = gui;
    self.loginHandler = loginHandler;
    self.loginDone = "";
    
    self.plus_user = plus_user;
    self.rootLink = "http://www.gamestar.de/";
    self.shortName = "GS";

    ##setup regular expressions
    self.regexVideoObject = re.compile("<a href=\"(/videos/.*?,\\d*?\\.html)\" title=\"(.*?)\">\\s*<img src=\"(.*?)\"");
    self.regexLink = re.compile("/videos/media,\\d+?(,(\\d)){0,1}\\.html");
        
    self.magazineVideoLinkRegex =  "(/plus/heftvideos/.*?,\\d*?,\\d*?\\.html)"
    self.magazineVideoHrefRegex = "<a.*? href=\""+self.magazineVideoLinkRegex+"\">"
    self.magazineVideoHeaderRegex = "<b>.+</b>\\s*.*\\s*</a>"
    
    self.imageRegex = "<img src=\".*\" width=\"\\d*\" height=\"\\d*\" alt=\".*\" (title=\".*\" )?/>"
    self._regEx_magazineVideoExtractMagID = re.compile("<div class=\"teaserHead\">\\s*<h3>(.*)</h3>\\s*<div style=\"clear:both\"></div>\\s*</div>");
    self._regEx_magazineVideoExtractNextPage = re.compile("<div style=\".*\">\\s*<a href=\"/index.cfm\?pid=2336.*pk=([0-9]*)\" class=\"linkProductM\">ältere Ausgaben</a>\\s*</div>");
    self._regEx_magazineVideoExtractVideoThumbnail = re.compile("<div class=\"teaserItem\".*>\\s*<div class=\"teaserImage\">\\s*"+self.magazineVideoHrefRegex+"\\s*"+"(<img class=\"pOverlay\"[^>]*>)?"+"\\s*"+self.imageRegex+"\\s*<span class=\"play\"></span>\\s*</a>\\s*</div>\\s*<div class=\"teaserTitle\">"+self.magazineVideoHrefRegex+"\\s*"+self.magazineVideoHeaderRegex);    
    self._regEx_magazineVideoExtractHeader = re.compile(self.magazineVideoHeaderRegex);
    self._regEx_extractVideoID = re.compile("(\\d*.html|pk=\\d*)");
    self._regEx_extractVideoLink = re.compile("http.*(mp4|flv)");
    self._regEx_extractPictureLink = re.compile("(http://|//).*.jpg");    
    
    ##end setup
    
    videoLinkRoot = self.rootLink+"videos/";        
    magazineVideoLinkRoot = self.rootLink+"index.cfm?pid=2336";
    imageRoot = "http://images.gamestar.de/images/idgwpgsgp/bdb/";        

    ##setup categories
    self.categories = {
#      20001:GalleryObject(videoLinkRoot+"search", imageRoot+"/2018270/b144x81.jpg","","search",True),
      
      21001:GalleryObject(magazineVideoLinkRoot, imageRoot+"/2018270/b144x81.jpg","","",False),
      
      30001:GalleryObject(videoLinkRoot+"alle-videos,9100,newest/", imageRoot+"/2018270/b144x81.jpg","","",True),
      
      30070:GalleryObject(videoLinkRoot+"alle-videos,9100,hot/", imageRoot+"/2018270/b144x81.jpg","","",True),
#      30071:GalleryObject(videoLinkRoot+"comments", imageRoot+"/2018270/b144x81.jpg","","",True),
      
      30002:GalleryObject(videoLinkRoot+"tests,17/",imageRoot+"2018272/b144x81.jpg","","",True),
      30003:GalleryObject(videoLinkRoot+"previews,18/",imageRoot+"bdb/2018269/b144x81.jpg","","",True),
      30004:GalleryObject(videoLinkRoot+"specials,20/",imageRoot+"2018270/b144x81.jpg","","",True),
#      30005:GalleryObject(videoLinkRoot+"9",imageRoot+"bdb/2016676/b144x81.jpg","","",True),
#      30006:GalleryObject(videoLinkRoot+"22",imageRoot+"2016431/b144x81.jpg","","",True),
      30007:GalleryObject(videoLinkRoot+"server-down-show,15/",imageRoot+"2018271/b144x81.jpg","","",True),
#      30008:GalleryObject(videoLinkRoot+"37",imageRoot+"2121485/b144x81.jpg","","",True),
      30009:GalleryObject(videoLinkRoot+"technik-checks,32/",imageRoot+"2018270/b144x81.jpg","","",True),
      30010:GalleryObject(videoLinkRoot+"boxenstopp,2/",imageRoot+"2018274/b144x81.jpg","","",True),
      30011:GalleryObject(videoLinkRoot+"trailer,3/",imageRoot+"2017073/b144x81.jpg","","",True),
      
      30080:GalleryObject(videoLinkRoot+"frisch-gestrichen,104/",imageRoot+"2622016/b144x81.jpg","","",True),
      30081:GalleryObject(videoLinkRoot+"was-ist-,96/","http://news.bbcimg.co.uk/media/images/77759000/jpg/_77759910_question-mark.jpg","","",True),
      30082:GalleryObject(videoLinkRoot+"news,100/",imageRoot+"2558457/b144x81.jpg","","",True),
      30083:GalleryObject(videoLinkRoot+"gamewatch,97/",imageRoot+"2510018/b144x81.jpg","","",True),
      30084:GalleryObject(videoLinkRoot+"monats-vorschau,24/",imageRoot+"2095504/b144x81.jpg","","",True),
#      30085:GalleryObject(videoLinkRoot+"23",imageRoot+"2017085/b144x81.jpg","","",True),
      30086:GalleryObject(videoLinkRoot+"gamestar-tv,1/", imageRoot+"2491153/b144x81.jpg","","",True),
      
      
      }
      
    import xml.dom.minidom
    linksXML = xml.dom.minidom.parse(urllib.urlopen("http://chb80.spdns.org/binaries/show_dynbin.php4?dynbin_id=PLUGIN_VIDEO_CHB80_GAMESTAR_LINKS_GS"))
    for mainNode in linksXML.childNodes:
      if mainNode.nodeName == "links":
        for linkNode in mainNode.childNodes:
          if linkNode.nodeName == "link":
            id = int(linkNode.getAttribute("id")) + 9000000
            for attributeNode in linkNode.childNodes:
              if attributeNode.nodeName == "link":
                link = attributeNode.firstChild.data.strip()
              elif attributeNode.nodeName == "imagelink":
                imagelink = attributeNode.firstChild.data.strip()
              elif attributeNode.nodeName == "title":
                title = attributeNode.firstChild.data.strip()
            if(link.startswith('http://')):
              self.categories[id]=GalleryObject(link, imageRoot+imagelink,title,"",True);
            elif(link.startswith('https://')):
              self.categories[id]=GalleryObject(link, imageRoot+imagelink,title,"",True);
            else:
              self.categories[id]=GalleryObject(videoLinkRoot+link, imageRoot+imagelink,title,"",True);            
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
    
    if categorieid in self.categories:
      categorie = self.categories[categorieid];
      executed = True
      categorie_url = categorie.url;
      
      if(categorieid == 21001):
        if(page > 1):
          categorie_url += "&pk=%s"%page;
      else:
        if(not categorie.userstring_parameter == ""):
          categorie_url += "&"+categorie.userstring_parameter+"="+userstring;
        if(page > 1):
          categorie_url += "&p=%s"%page;
        
      self.gui.log(categorie_url);
      rootDocument = self.loadPage(categorie_url);      
      
      if(categorieid == 21001):
        for videoThumbnail in self._regEx_magazineVideoExtractVideoThumbnail.finditer(rootDocument):
          
          videoThumbnail = videoThumbnail.group()        
          videoID = self._regEx_extractVideoID.search(videoThumbnail).group().replace(".html","").replace("pk=","");
          
          header = self._regEx_magazineVideoExtractHeader.search(videoThumbnail).group();
          header = re.sub("(<b>)|(</b>)|(</a>)", "", header);
          header = re.sub("\\s+", " ", header);
          
          try:
            videoObjects.append(self.loadVideoPage(header, videoID));            
          except:
            self.gui.log("something goes wrong while processing "+videoID);
        self.gui.log("Exception: ");
        traceback.print_exc();
        self.gui.log("Stacktrace: ");
        traceback.print_stack();   
      else:
        videoIds = set();
        for match in self.regexVideoObject.finditer(rootDocument):
          title = match.group(2);
          thumbnailLink = match.group(3);
          if(not thumbnailLink.startswith('http://')):
            thumbnailLink = thumbnailLink.replace("//",'http://');
          videoPageLink = self.rootLink+match.group(1);
          self.gui.log(videoPageLink);
          videoPage=self.loadPage(videoPageLink);
          matches= list(self.regexLink.finditer(videoPage));
          if len(matches) == 0: 
            continue;
          if len(matches) == 1:
            link = self.rootLink+matches[0].group(0);
          else:
            links = {}
            for match in self.regexLink.finditer(videoPage):
              quality = match.group(1);
              link = self.rootLink+match.group(0);
              self.gui.log("Quality %s: %s"%(quality,link));
              links[quality]=link
            qualitiy = sorted(links.keys(),reverse = True)[0];
            link=links[qualitiy]
          videoObjects.append(VideoObject(title, link, thumbnailLink, self.shortName));
          
      if(categorieid == 21001):
        newpage = self._regEx_magazineVideoExtractNextPage.search(rootDocument).group(1);
        newpagetext = addon.getLocalizedString(30900)+" "+self._regEx_magazineVideoExtractMagID.search(rootDocument).group(1);
      else:
        newpage = page + 1
        newpagetext = ""
        
    return {'videoObjects':videoObjects, 'executed':executed, 'newpage':newpage, 'newpagetext':newpagetext }

  def loadVideoObject(self, videoID):
    link = self.configPage%videoID;
    self.gui.log(link);
    configDoc = self.loadPage(link).decode('utf-8');
    videoLink = self._regEx_extractVideoLink.search(configDoc).group();
    videoLink = self.replaceXmlEntities(videoLink);
    thumbnailLink = self._regEx_extractPictureLink.search(configDoc).group();
    title = self._regEx_extractTitle.search(configDoc).group(1);
    title = self.transformHtmlCodes(title);
    if(not thumbnailLink.startswith('http://')):
      thumbnailLink = thumbnailLink.replace("//",'http://');
    thumbnailLink = thumbnailLink;
    
    return VideoObject(title, videoLink, thumbnailLink, self.shortName)
  
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
      login_state = self.login(self.plus_user)      
    
      safe_url = url.replace( " ", "%20" ).replace("&amp;","&")
      doc = self.loginHandler.opener.open(safe_url).read()
      #sock = urllib.urlopen( safe_url )
      #doc = sock.read()
      if doc:
        return doc
      else:
        return ''
    except:            
      return ''
      
  def login(self,user):        
    if user=="":
      return "none"
    elif self.loginDone=="":    
      self.gui.log("checking Gamestar login for user: "+user)
      content = self.loginHandler.opener.open(self.rootLink+"index.cfm?pid=832&op=1023").read()      
      
      if 'Kontrollzentrum für '+user in content:
        self.loginDone = "plus"
      else:
        try:
          self.gui.log("logging in...")
          content = ""                            
          br = mechanize.Browser()
          br.set_cookiejar(self.loginHandler.cj)
          br.set_handle_robots(False)
          br.addheaders = [('User-agent', self.loginHandler.userAgent)]
          content = br.open(self.rootLink+"index.cfm?pid=103&op=10")
          br.select_form(name="login")
          br["username"] = user
          br["password"] = self.loginHandler.addon.getSetting('gamestar_plus_pass')
          br["loginstayonline"] = ["1"]
          content = br.submit().read()
          self.loginHandler.cj.save(self.loginHandler.cookieFile)
          content = self.loginHandler.opener.open(self.rootLink+"index.cfm?pid=832&op=1023").read()
        except:
          content = ""
          traceback.print_exc();
        if 'Kontrollzentrum für '+user in content:
          self.loginDone = "plus"        
        else:
          self.loginDone = "none"
      
      self.gui.log("login state for user: "+self.loginDone)
      return self.loginDone
    else:
      return self.loginDone

  
  def loadVideoPage(self, title, videoID):
    self.gui.log(self.rootLink+"/emb/getVideoData.cfm?vid="+videoID);
    configDoc = self.loadPage(self.rootLink+"/emb/getVideoData.cfm?vid="+videoID);
    videoLink = unicode(self._regEx_extractVideoLink.search(configDoc).group());
    videoLink = self.replaceXmlEntities(videoLink);
    thumbnailLink = self._regEx_extractPictureLink.search(configDoc).group();
    if(not thumbnailLink.startswith('http://')):
      thumbnailLink = thumbnailLink.replace("//",'http://');
    thumbnailLink = unicode(thumbnailLink);
    
    return VideoObject(title, videoLink, thumbnailLink, self.shortName);