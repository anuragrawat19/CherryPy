import cherrypy
from config import  LOG_CONF
import logging
import logging.config
logger = logging.getLogger()
db_logger = logging.getLogger('db')



class Blog(object):
    @cherrypy.expose
    dd = "jhj"
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
    def index(self):
        logger.info('boom')
        db_logger.info('bam')
        cherrypy.log("hello there") # for logging the errors
        cherrypy.response.cookie["seckret_key"]="asdasdasdasda"
        google_appid = {"naam":"Anurag"}
        return cherrypy.request.cookie["seckret_key"]

cherrypy.config.update({'server.socket_port': 9090})
cherrypy.config.update({'log.screen':False,
                        'log.access_file':'',
                        'log.error_file':''})
cherrypy.engine.unsubscribe('graceful',cherrypy.log.reopen_files)
logging.config.dictConfig(LOG_CONF)

''' cherry/.tree.mount  is for muliple application'''
cherrypy.tree.mount(Forum(), '/forum')
cherrypy.tree.mount(Blog(), '/blog')
cherrypy.tree.mount(Root(),'/root')

cherrypy.engine.start()
cherrypy.engine.block()

