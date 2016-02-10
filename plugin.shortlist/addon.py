#!/usr/bin/python

import os
import json
import xbmc
import xbmcaddon
import xbmcgui

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name').decode('utf-8')
__localize__ = __addon__.getLocalizedString

tag = __addon__.getSetting('tag')
id = xbmc.getInfoLabel('ListItem.DBID');

def getTags():
    cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": %s, "properties": ["tag"]}, "id": 1}'
    cmd = cmd %(id)
    result = json.loads(xbmc.executeJSONRPC(cmd))
    return result['result']['moviedetails']['tag']

def addTag(tag):
    tags = getTags()
    if tag not in tags:
        tags.append(tag)
        cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid": %s, "tag": %s}, "id": 1}'
        cmd = cmd %(id, json.dumps(tags))
        result = xbmc.executeJSONRPC(cmd)

def removeTag(tag):
    tags = getTags()
    if tag in tags:
        tags.remove(tag)
        cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid": %s, "tag": %s}, "id": 1}'
        cmd = cmd %(id, json.dumps(tags))
        result = xbmc.executeJSONRPC(cmd)

item = xbmcgui.Dialog().select(__addonname__, [
    __localize__(30002) %(tag),
    __localize__(30003) %(tag)
])

if item == 0:
    addTag(tag)
elif item == 1:
    pos = int(xbmc.getInfoLabel('Container.CurrentItem'))
    win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    ctl = win.getControl(win.getFocusId())
    removeTag(tag)
    xbmc.executebuiltin('Container.Refresh()', True)
    ctl.selectItem(pos)
    # Have to use xbmc.getInfoLabel as ctl.getListItem does not work for builtin lists
    new_id = xbmc.getInfoLabel('ListItem.DBID');
    if new_id != id and pos > 1:
        pos = pos - 1
    ctl.selectItem(pos)
