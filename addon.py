import os
import json

import xbmc
import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
tag = addon.getSetting('tag')
id = xbmc.getInfoLabel('ListItem.DBID');

# Get tags
cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": %s, "properties": ["tag"]}, "id": 1}'
cmd = cmd %(id)
result = json.loads(xbmc.executeJSONRPC(cmd))
tags = result['result']['moviedetails']['tag']

# Add shortlist tag to list of tags if not already in
if tag not in tags:
    tags.append(tag)

# Set tags
cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid": %s, "tag": %s}, "id": 1}'
tags = json.dumps(tags)
cmd = cmd %(id, tags)
result = xbmc.executeJSONRPC(cmd)

'''
line1 = 'Id: ' + xbmc.getInfoLabel('ListItem.DBID')
line2 = 'Tags: ' + ', '.join(tags) 
line3 = 'Args: ' + ', '.join(sys.argv)

xbmcgui.Dialog().ok(addonname, line1, line2, line3)
''' 
