# -*- coding: utf-8 -*-
#-------------LicenseHeader--------------
# plugin.video.gamestar - Downloads/view videos from gamestar.de
# Copyright (C) 2010  Raptor 2101 [raptor2101@gmx.de]
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
import os,xbmcgui,urllib,urllib2,re;
from gamestar import GamestarWeb
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

rootPath = os.getcwd();
configFilePath = os.path.join(rootPath,"config");
archivePath = None
forcedPrecachingConfig = None
if(os.path.exists(configFilePath)):
  configFile = open(configFilePath,"r");
  for line in configFile.readlines():
    if(line.startswith("cachePath=")):
      archivePath = line.replace("cachePath=","").rstrip();
    if(line.startswith("forcePrecaching=")):
      forcedPrecachingConfig = line.replace("cachePath=","");

gui = SimpleXbmcGui(archivePath);
webSite=GamestarWeb(gui);

gui.openMenuContext();
params=get_params()
action=params.get("action", "")
cat=int(params.get("cat", 0))
gui.log("action: "+action);

if(action == "list"):
  forcedPrecaching = forcedPrecachingConfig is not None and forcedPrecachingConfig.find("%d;"%cat)>-1;
  category = webSite.categories[cat];
  webSite.builCategoryMenu(category.url,forcedPrecaching);
elif(action == "download"):
  gui.download(params.get("url", ""));
  gui.refresh();
elif(action == "downloadPlay"):  
  mediaPath = gui.download(params.get("url", ""));
  gui.play(mediaPath);
  gui.refresh();
else:
  webSite.buildCategoryMenu();

gui.closeMenuContext();