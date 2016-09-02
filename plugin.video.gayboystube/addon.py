# The documentation written by Voinage was used as a template for this addon
# http://wiki.xbmc.org/?title=HOW-TO_write_plugins_for_XBMC
#
# This addon is licensed with the GNU Public License, and can freely be modified
# http://www.gnu.org/licenses/gpl-2.0.html

import urllib
import urllib2
import re
import xbmcplugin
import xbmcgui
import xbmcaddon
import CommonFunctions
import cookielib

common = CommonFunctions
common.plugin = "plugin.video.gayboystube-1.0.2"
cookiejar = cookielib.LWPCookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_handler)

# debugging
common.dbg = False #Default
common.dbglevel = 3 # Default = 3

# xbmc hooks
__settings__ = xbmcaddon.Addon( id="plugin.video.gayboystube" )

# examples i'm working from always define functions before the main program code, so I'm assuming that's a requirement.

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                                
    return param

def displayRootMenu():
    addListItem('Latest Videos','most-recent/','scrapeVideoList','DefaultFolder.png')
    addListItem('Random Videos','random/','scrapeVideoList','DefaultFolder.png')
    addListItem('Top Rated Videos','top-rated/','scrapeVideoList','DefaultFolder.png')
    addListItem('Top Favorites','top-favorites/','scrapeVideoList','DefaultFolder.png')
    addListItem('Most Viewed','most-viewed/','scrapeVideoList','DefaultFolder.png')
    addListItem('Most Commented','most-discussed/','scrapeVideoList','DefaultFolder.png')
    # todo: channels; search


def addListItem(name,url,mode,iconimage,page="page1.html",duration=0):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)+"&page="+urllib.quote_plus(page)
    ok=True
    if mode=='scrapeVideoList':
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    elif mode=='playVideo':
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "duration": duration } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok


def indexVideos(path,page):
     result = common.fetchPage({"link": base_url + path + page})
     if result["status"] != 200:
          print "bad url passed to function indexVideos"
     content = result["content"]
     items = common.parseDOM(content, "div", attrs = {"class": "item"})
     link = common.parseDOM(items, "a", attrs = {"class": ""}, ret="href")
     image = common.parseDOM(items, "img", ret="src")
     title = common.parseDOM(items, "img", ret="alt")
     length = common.parseDOM(items, "div", attrs = {"class": "duration"})
     for i, link2 in enumerate(link):
          name = common.makeAscii(common.replaceHTMLCodes(title[i]))
          addListItem(name=name, url=urllib.quote_plus(link2), mode='playVideo', iconimage=image[i], page=page, duration=length[i])
     nextpage = common.parseDOM(content, "a", attrs={"class": "next"}, ret="href")
     if path != "random/":
          addListItem(name="Go to next page", url=path, mode='scrapeVideoList', iconimage='DefaultFolder.png', page=nextpage[len(nextpage)-1])


def playVideo(url,name,thumb):
    req = urllib2.Request(urllib.unquote_plus(url))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('file: \'([A-Za-z0-9_/.:-?&= _]*)\',').findall(link)
    for url in match:
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        listitem.setThumbnailImage(urllib.unquote_plus(thumb))
       	xbmc.Player().play(url, listitem)


# initialize variables
url=None
name=None
thumb=None
mode=None
page=None

# get parameters passed through plugin URL
params=get_params()

# set any parameters that were passed through the plugin URL
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    thumb=urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    mode=urllib.unquote_plus(params["mode"])
except:
    pass
try:
    page=urllib.unquote_plus(params["page"])
except:
    pass


# ok - the parameters are initialized where are we scraping?
base_url='http://www.gayboystube.com/'
categories_url=base_url + 'channels/'
search_url=base_url + 'search/videos/'

# log some basics to the debug log for funzies.
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
    print base_url
    displayRootMenu()
       
elif mode=='scrapeVideoList':
    print ""+url+page
    indexVideos(url,page)
        
elif mode=='playVideo':
    print ""+url
    playVideo(url,name,thumb)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
