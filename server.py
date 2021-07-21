import cherrypy
from subject6.app import app

""" Production CherryPy server """

if __name__ == '__main__':
    cherrypy.config.update({
        'global': {'environment' : 'production'}
    })

    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.server.unsubscribe()

    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = 5000
    server.thread_pool = 30
    server.subscribe()

    cherrypy.engine.signal_handler.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
