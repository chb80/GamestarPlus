# -*- coding: utf-8 -*-
#-------------LicenseHeader--------------
# plugin.video.chb80_gamestar - Downloads/view videos from gamestar.de
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
import os,xbmcgui,urllib,urllib2,re,xbmcaddon,mechanize, cookielib;
from gamestar import GamestarWeb
from gamepro import GameproWeb
from simplexbmc import SimpleXbmcGui;


def get_params():
  """ extract params from argv[2] to make a dict (key=value) """
  paramDict = {}
  try:
    print "get_params() argv=", sys.argv
    if sys.argv[2]:
      paramPairs=sys.argv[2][1:].split( "&" )
      for paramsPair in paramPairs:
        paramSplits = paramsPair.split('=')
    if (len(paramSplits))==2:
      paramDict[paramSplits[0]] = paramSplits[1]
  except:
    errorOK()
  return paramDict

__settings__ = xbmcaddon.Addon(id='plugin.video.chb80_gamestar')
rootPath = __settings__.getAddonInfo('path');

displayGamestar = __settings__.getSetting('gamestar') == "true";
displayGamepro = __settings__.getSetting('gamepro') == "true";
displayYoutube = __settings__.getSetting('youtube') == "true";
showSourcename = __settings__.getSetting('show_shortname') == "true";
GamestarPlusUser = __settings__.getSetting('gamestar_plus');

gui = SimpleXbmcGui(showSourcename);


gui.openMenuContext();
params=get_params()
action=params.get("action", "")
cat=int(params.get("cat", 0))
if(cat == 21001): ##magazine videos, does paging based on external number
  page=int(params.get("page", 0))
else: 
  page=int(params.get("page", 1))
userstring=params.get("userstring", "")

if(userstring == ""):
  if(cat == 20001): ##search
    result = gui.keyboardInput();
    if (result.isConfirmed()):
      userstring = unicode(result.getText().decode('UTF-8'));
  
gui.log("action: "+action);
gui.log("cat: %s"%cat);
gui.log("page: %s"%page);
gui.log("userstring: %s"%userstring);



class Login(object):
  def __init__(self,settings):
    self.addon = settings
    self.addonID = self.addon.getAddonInfo('id')
    self.addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+self.addonID).decode('utf-8')
    
    self.cj = cookielib.MozillaCookieJar()
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
    self.userAgent = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0"
    
    self.opener.addheaders = [('User-agent', self.userAgent)]
    
    self.cookieFile = os.path.join(self.addonUserDataFolder, "cookies")
    
    if not os.path.isdir(self.addonUserDataFolder):
      os.mkdir(self.addonUserDataFolder)
    if os.path.exists(self.cookieFile):
      self.cj.load(self.cookieFile)


loginHandler = Login(__settings__)


  
if(action == "list"):
  videoObjects = [];  
  newpage = 0;
  newpagetext = "";
  
  if(displayGamestar):
    website = GamestarWeb(gui,loginHandler,GamestarPlusUser);
    result=website.getVideoLinkObjects(cat, page, userstring);
    
    if(result['executed']):
      newpage=result['newpage'];
      newpagetext=result['newpagetext'];      
      videoObjects.extend(result['videoObjects'])
      
  if(displayGamepro):
    website = GameproWeb(gui,loginHandler);
    result = website.getVideoLinkObjects(cat, page, userstring);
    
    if(result['executed']):
      newpage=result['newpage'];
      newpagetext=result['newpagetext'];      
      videoObjects.extend(result['videoObjects'])
    
    
  gui.buildVideoLink(cat, videoObjects);  
  gui.buildNextPageLink(cat, newpage, userstring, newpagetext);
else:
  categories = {};
  if(displayGamestar):
    website = GamestarWeb(gui,loginHandler,GamestarPlusUser);
    categories.update(website.getCategories())    
  if(displayGamepro):
    website = GameproWeb(gui,loginHandler);
    categories.update(website.getCategories())        
  gui.showCategories(categories);

gui.closeMenuContext();
