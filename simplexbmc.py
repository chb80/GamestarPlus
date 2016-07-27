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
import xbmc, xbmcgui, xbmcplugin,xbmcaddon, sys, urllib, urllib2, os, re, time
__plugin__ = "Gamestar"

regex_getTargetPath = re.compile("[^/]*\\..{3}$");

class SimpleXbmcGui(object):
  def __init__(self, showSourcename):
    self.showSourcename = showSourcename;
    
  def log(self, msg):
    if type(msg) not in (str, unicode):
      xbmc.log("[%s]: %s" % (__plugin__, type(msg)))
    else:
      xbmc.log("[%s]: %s" % (__plugin__, msg.encode('utf8')))
    
  def buildVideoLink(self, category, videoItems):
    for videoItem in videoItems:
      if(self.showSourcename):
        title = "[%s] %s"%(videoItem.sourceName, videoItem.title)
      else:
        title = "%s"%(videoItem.title)
      listItem=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=videoItem.picture)
            
      url = videoItem.url;
      xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=listItem,isFolder=False)    
        
  def buildNextPageLink(self, category, page, userstring, newpagetext):        
    if(newpagetext == ""):
      title = ">>> %s >>>"%page
    else:
      title = ">>> %s >>>"%newpagetext
      
    listItem=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage="")
    url = "%s?&action=list&cat=%s" % (sys.argv[0], category);
    if(not userstring == ""):
      url += "&userstring=%s"%userstring;
    if(page > 0):
      url += "&page=%s"%page;
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=listItem,isFolder=True)    

  def showCategories(self,categorieItems):
    for index in categorieItems:    
      categorieItem = categorieItems[index]
      
      addon = xbmcaddon.Addon("plugin.video.chb80_gamestar")
      
      if(index<900000):
        tobeused_title = addon.getLocalizedString(index)
      else:
        tobeused_title = categorieItem.title
        
      listItem=xbmcgui.ListItem(tobeused_title, iconImage="DefaultFolder.png", thumbnailImage=categorieItem.pictureLink)
      #listItem.setInfo('', { 'count': index })
      if(categorieItem.default_paging):
        u = "%s?&action=list&cat=%s&page=%s" % (sys.argv[0], index, 1)
      else:
        u = "%s?&action=list&cat=%s" % (sys.argv[0], index)
        
      xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=listItem,isFolder=True)
    
    #xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=20)
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=1)
  
  def openMenuContext(self):
    self.dialogProgress = xbmcgui.DialogProgress();
  
  def closeMenuContext(self):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
  def refresh(self):
    xbmc.executebuiltin("Container.Refresh");
  
  def play(self, path):
    player = xbmc.Player();
    player.play(path);
    
  def keyboardInput(self):
    keyboard = xbmc.Keyboard("")
    keyboard.doModal();
    return keyboard;
  
  def errorOK(self,title="", msg=""):
    e = str( sys.exc_info()[ 1 ] )
    self.log(e)
    if not title:
      title = __plugin__
    if not msg:
      msg = "ERROR!"
    if(e == None):
      xbmcgui.Dialog().ok( title, msg, e )  
    else:
      xbmcgui.Dialog().ok( title, msg)  
