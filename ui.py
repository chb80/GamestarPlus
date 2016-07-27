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
class VideoObject(object):
  def __init__(self, title, url, picture, sourceName):
    self.title = title
    self.url = url
    self.picture = picture
    self.sourceName = sourceName

class GalleryObject(object):
  def __init__(self,url,pictureLink,title,userstring_parameter,default_paging):
    self.url = url
    self.pictureLink = pictureLink
    self.title = title
    self.userstring_parameter = userstring_parameter
    self.default_paging = default_paging
