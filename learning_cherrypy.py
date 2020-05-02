import cherrypy
from config import  LOG_CONF
import glob
import os.path
import logging
import logging.config
logger = logging.getLogger()
db_logger = logging.getLogger('db')

#Basic Understanding of Cherrypy

class Blog(object):
    @cherrypy.expose
    def index(self):
        return "Hello THis my First Blog................"

''' cherry.quickstart is only for single application'''
# cherrypy.quickstart(Blog(),'/blog',{'/': {'tools.gzip.on': True}}) 

class Forum(object):
    @cherrypy.expose
    def index(self):
        return "THis is the forum "


class Root(object):
    @cherrypy.expose
    def index(self, directory="."):
        html = """<html><body><h2>Here are the files in the selected directory:</h2>
        <a href="index?directory=%s">Up</a><br />
        """ % os.path.dirname(os.path.abspath(directory))

        for filename in glob.glob(directory + '/*'):
            absPath = os.path.abspath(filename)
            if os.path.isdir(absPath):
                html += '<a href="/index?directory=' + absPath + '">' + os.path.basename(filename) + "</a> <br />"
            else:
                html += '<a href="/download/?filepath=' + absPath + '">' + os.path.basename(filename) + "</a> <br />"

        html += """</body></html>"""
        return html

class MyCookieApp(object):
    @cherrypy.expose
    def set(self):
        cookie = cherrypy.response.cookie
        print (cookie)
        cookie['userid'] = '12'
        cookie["path"] = "127.0.0.2/cookies"
        
        return "<html><body>Hello, I just sent you a cookie</body></html>"
    @cherrypy.expose
    def index(self):
        cookie = cherrypy.request.cookie
        res = """<html><body>Hi, you sent me %s cookies.<br />
                Here is a list of cookie names/values:<br />""" % len(cookie)
        for name in cookie.keys():
            res += "name: %s, value: %s<br>" % (name, cookie[name].value)
        return res + "</body></html>"


#allow Files downlaoding
from cherrypy.lib.static import serve_file
class Downloading(object):
    @cherrypy.expose
    def index(self,filepath):
        return serve_file(filepath,"application/x-download",'attachment')
    

#for encoding the json data
class Jsondata(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"key":"Value"}



'''Configuration for the serever'''        
cherrypy.config.update({'server.socket_port': 9090})
cherrypy.config.update({'log.screen':False,
                        'log.access_file':'',
                        'log.error_file':''})
cherrypy.engine.unsubscribe('graceful',cherrypy.log.reopen_files)
logging.config.dictConfig(LOG_CONF)

''' cherry/.tree.mount  is for muliple application'''
#routes defined
cherrypy.tree.mount(Downloading(), '/download')
cherrypy.tree.mount(Forum(), '/forum')
cherrypy.tree.mount(Blog(), '/blog')
root = Root()
root.download = Downloading()
cherrypy.tree.mount(root,'/root')
cherrypy.tree.mount(MyCookieApp(),'/cookies')
cherrypy.tree.mount(Jsondata(),"/jsondata")

cherrypy.engine.start()
cherrypy.engine.block()

