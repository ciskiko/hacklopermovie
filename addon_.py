#-*-coding:utf-8-*-
import sys,os,re, logging,urllib2,urllib,ast
import search
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import logging

load_movies = 'https://dl.dropboxusercontent.com/u/30418660/kodi_movies/'

f = urllib2.urlopen('https://dl.dropboxusercontent.com/u/30418660/kodi_movies/var.txt').read()
var = ast.literal_eval(f)

for v in var:
    exec("{0}=[]".format(v))

class Addon(object):
    def __init__(self):
        self._addon = xbmcaddon.Addon()
        self._home = xbmc.translatePath(self._addon.getAddonInfo('path'))

    def check_url(self,url):
        logging.warning("check_url "+str(url))
        try:
            u = re.match(r'[^:]+',url).group()
            if u == 'http' or u == 'https':
                return True
            return False
        except:
            return False

    def connect_next_menu(self,tag):
        handle = int(sys.argv[1])
        xbmcplugin.setContent(handle,"windows")
        logging.warning("tag original principio: "+str(tag))
        if 'tag=idiomas' in tag:
            lang_url = [i.split('=') for i in tag[1:].split('&')[:-1]]
            logging.warning("lang_url -----> "+str(lang_url))
            self.set_list('idiomas')
            tag = eval('idiomas')
            for v in tag:
                logging.warning("v vale ----->: "+str(v))
                try:
                    url = [i[1] for i in lang_url if i[0]==v['id']][0]
                except IndexError:
                    url = ''
                if 'streamcloud.eu' in url:
                        url = self.streamCloud(url)

                name = v['name'].replace("\xf1","ñ")
                logging.warning("url idiomas ----->"+str(v['name']+'------>')+str(url))
                logging.warning("tipo ----------->"+str(type(v['name'])))
                item = xbmcgui.ListItem(name,iconImage=v['icon'])
                xbmcplugin.addDirectoryItem(handle=handle,url=url,listitem=item)

        else:
            tag = eval(tag)
            for v in tag:
                #icon = os.path.join(self._home,'logos',v['icon'])
                icon = v['icon']
                #farnat = os.path.join(self._home,'farnats',v['fanart'])
                farnat = v['fanart']
                item = xbmcgui.ListItem(v['name'],iconImage=icon)
                item.setProperty('fanart_image',farnat)
                if self.check_url(v['url']) == False:

                    url = sys.argv[0]+'?tag='+str(v['url'])
                    xbmcplugin.addDirectoryItem(handle=handle,url=url,listitem=item,isFolder=True)
                else:
                    url = v['url']
                    if 'streamcloud.eu' in url:
                        url = self.streamCloud(url)
                    logging.warning("v entero: "+str(v))
                    logging.warning("url nueva--->"+str(v['name'])+"------>"+str(url))
                    xbmcplugin.addDirectoryItem(handle=handle,url=url,listitem=item)

        xbmcplugin.endOfDirectory(handle)

    def start(self):
        tag = self.get_params()
        if tag == None:
            self.start_menu()
        else:
            self.connect_next_menu(tag)

    def get_params(self):
        param = urllib.unquote(sys.argv[2])
        logging.warning("original param: "+str(param))
        if param:
            if 'tag=idiomas' in param:
                return param
            else:
                logging.warning("error eval--->"+str(param))
                name = param[5:]
                self.set_list(name)
                return name
        else:
            return None

    def streamCloud(self,url):
        logging.warning("url streamcloud -------------->"+str(url))
        try:
            obj = search.streamCloud(url)
            resp = obj.run()
            return resp
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("Archivo no encontrado","no se encuentra el archivo avise al moderador")
    def set_list(self,name):
        logging.warning("set_list name: "+str(name))
        f = urllib2.urlopen(load_movies+name.lower()+'.txt').read()
        exec(f.replace("\r\n",""))
        globals()[name] = eval('{0}_'.format(name))

    def start_menu(self):
        handle = int(sys.argv[1])
        xbmcplugin.setContent(handle,'menu_principal')
        self.set_list('Menu')
        for text in Menu:
            icon = text['icon']
            #fanart = os.path.join(self._home,'farnats',text['fanart'])
            fanart = text['fanart']
            if icon:
                logging.warning("entra en icon ---------->"+str(icon))
                item = xbmcgui.ListItem(text['name'],iconImage=icon)
            else:
                icon = os.path.join(self._home,'logos',text['icon'])
                item = xbmcgui.ListItem(text['name'],iconImage=icon)
            item.setProperty('fanart_image',fanart)
            url = sys.argv[0]+'?tag='+str(text['url'])
            xbmcplugin.addDirectoryItem(handle=handle,url=url,listitem=item,isFolder=True)
        xbmcplugin.endOfDirectory(handle)

addon = Addon()
addon.start()