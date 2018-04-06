#!/usr/bin/env python
# coding=utf-8

"""
The web interface.

(for cherrypy server)

URI structure:
    '/' --> static content (index.html)
    '/api' api root
        sub calls see web_api.py file.
"""

from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division


# import sys
import os
# import pprint
# import traceback

import cherrypy

import modules.configdict as configdict
# from modules.exception_classes import FormatError

from web_api import APIHandler


class StaticFiles(object):
    """StaticFiles Class - Only here to have a class..."""

    pass


class InterfaceWeb(object):
    """Interactive commandline interface."""

    dir_current = os.path.dirname(os.path.abspath(__file__))

    config_defaults = {
        "path": "./config/",
        "cherrypy": {
            "global": {
                # "server.socket_host": "::",
                "server.socket_host": "0.0.0.0",
                "server.socket_port": 8081,
                # "server.socket_port": 80,
                "server.environment": "development",
                # "server.environment": "production",
                "server.thread_pool": 20,
            },
        }
    }

    def __init__(self, config, verbose=False, parent=None):
        """Init main Application Class."""
        # object.__init__(self)
        super(InterfaceWeb, self).__init__()
        self.verbose = verbose
        self.parent = parent
        # setup termination and interrupt handling:
        # signal.signal(signal.SIGINT, self._exit_helper)
        # signal.signal(signal.SIGTERM, self._exit_helper)

        # extend config with defaults
        self.config = config
        configdict.extend_deep(self.config, self.config_defaults.copy())
        # print("config: {}".format(self.config))

        ##########################################
        # cherrypy initialization
        cherrypy.config.update(self.config["cherrypy"])
        # config static tool
        dir_static = os.path.join(self.dir_current, 'static')
        dir_logo = dir_static + '/img/logo'
        configStatic = {
            '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.root': dir_static,
                'tools.staticdir.dir': '',
                'tools.staticdir.index': 'index.html'
            },
            '/favicon.ico': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': dir_logo + '/logo.ico',
            },
            '/favicon.svg': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': dir_logo + '/logo.svg',
            },
            '/favicon.png': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': dir_logo + '/logo_500x500.png',
            },
        }
        # pp.pprint(configStatic)
        cherrypy.tree.mount(StaticFiles(), '', configStatic)

        ##########################################
        # cherrypy API

        configAPI = {
            '/': {
                # 'tools.sessions.on': True,
                # 'tools.json_in.on': True,
                # 'tools.json_out.on': True,
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            },
        }
        self.my_api_handler = APIHandler(self.verbose, self.parent)
        cherrypy.tree.mount(self.my_api_handler, '/api', configAPI)

    def __del__(self):
        """Clean up."""
        pass

    def start(self):
        """Start Cherrypy Engine."""
        print('******************************************')
        print('cherrypy server - start engine:')
        # cherrypy.engine.signals.subscribe()
        cherrypy.engine.start()
        # cherrypy.engine.block()

    def stop(self):
        """Stop Cherrypy Engine."""
        print('******************************************')
        print('cherrypy server - stop engine:')
        cherrypy.engine.exit()
        # cherrypy.engine.stop()

##########################################


##########################################
if __name__ == '__main__':
    import sys
    print(42 * '*')
    print('Python Version: ' + sys.version)
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    print("This Module has no stand alone functionality.")
    print(42 * '*')

##########################################
