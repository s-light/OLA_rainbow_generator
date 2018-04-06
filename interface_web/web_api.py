#!/usr/bin/env python
# coding=utf-8

u"""
The web interface.

Cherrypy API package.

(for cherrypy server)

'/api' api root
    '/brightness' GET UPDATE
    '/pattern_duration' GET UPDATE

Operations:
    (http://www.ibm.com/developerworks/library/ws-restful/index.html#N10066)
    - To create a resource on the server, use POST.
    - To retrieve a resource, use GET.
    - To change the state of a resource or to update it, use PUT.
    - To remove or delete a resource, use DELETE.

Error Codes:
    http://de.wikipedia.org/wiki/HTTP-Statuscode

    501 Not Implemented
    cherrypy.response.status = 501
    Die Funktionalität, um die Anfrage zu bearbeiten,
    wird von diesem Server nicht bereitgestellt.
    Ursache ist zum Beispiel eine unbekannte oder
    nicht unterstützte HTTP-Methode.

    404 Not Found
    cherrypy.response.status = 404
    Die angeforderte Ressource wurde nicht gefunden.

    403 Forbidden
    cherrypy.response.status = 403
    Die Anfrage wurde mangels Berechtigung
    des Clients nicht durchgeführt.

    420 Policy Not Fulfilled
    cherrypy.response.status = 420
    In W3C PEP (Working Draft 21. November 1997)[8]
    wird dieser Code vorgeschlagen, um mitzuteilen,
    dass eine Bedingung nicht erfüllt wurde.

    422 Unprocessable Entity
    cherrypy.response.status = 422
    Verwendet, wenn weder die Rückgabe von Statuscode 415 noch 400
    gerechtfertigt wäre, eine Verarbeitung der Anfrage jedoch
    zum Beispiel wegen semantischer Fehler abgelehnt wird.
"""

from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division

# import traceback

import cherrypy

# import modules.configdict as configdict


class APIHandler(object):
    """WEB API handler."""

    exposed = True

    def __init__(self, verbose=False, parent=None):
        """Init main Application Class."""
        object.__init__(self)
        self._verbose = verbose
        self._parent = parent
        # print('self._verbose', self._verbose)
        # print('self._parent', self._parent)
        self.brightness = Brightness(self._verbose, self._parent)
        self.pattern_duration = PatternDuration(self._verbose, self._parent)

    # @cherrypy.expose
    def GET(self):
        """Return some API example calls/information."""
        info = """
        <h1>Welcome to the API :-)</h1>
        <a href="../">../</a>
        <p>try to browse through the api by following these links:</p>
        <h2>Subparts:</h2>
        <ul>
            <li><a href="brightness/">brightness/</a></li>
            <li><a href="pattern_duration/">pattern_duration/</a></li>
        </ul>
        """
        return info

##########################################


class Brightness(object):
    """
    API Brightness.

        GET = receive current brightness
        PUT = set brightness

        "brightness": {
            "parameter": "parent.rainbow_generator.brightness",
            "parser_type": "int",
            "bounds": {
                "mode": "restrict",
                "min": 0,
                "max": 255,
            },
        },
    """

    exposed = True

    def __init__(self, verbose=False, parent=None):
        """Init."""
        self._verbose = verbose
        self._parent = parent

    @cherrypy.tools.json_in()
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self):
        """Get."""
        result = self._parent.rainbow_generator.brightness
        return result

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.popargs('value')
    def PUT(self, value=None):
        """Set."""
        jsondata = cherrypy.request.json
        result = {}
        try:
            if "value" in jsondata:
                value = jsondata["value"]
            self._parent.rainbow_generator.brightness = value
        except Exception as e:
            print(e)
            result = {
                "error": e.__dict__
            }
            # 422 Unprocessable Entity
            cherrypy.response.status = 422
        else:
            result = self._parent.rainbow_generator.brightness
        return result


class PatternDuration(object):
    """
    API PatternDuration.

        GET = receive current pattern_duration
        PUT = set pattern_duration

        "pattern_duration": {
            "parameter": "parent.rainbow_generator.pattern_duration",
            "parameter_unit": "s",
            "parser_type": "int",
            "bounds": {
                "mode": "restrict",
                "min": 1,
                "max": 10000,
            },
        },
    """

    exposed = True

    def __init__(self, verbose=False, parent=None):
        """Init."""
        self.verbose = verbose
        self._parent = parent

    @cherrypy.tools.json_in()
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self):
        """Get."""
        result = self._parent.rainbow_generator.pattern_duration
        return result

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.popargs('value')
    def PUT(self, value=None):
        """Set."""
        jsondata = cherrypy.request.json
        result = {}
        try:
            if "value" in jsondata:
                value = jsondata["value"]
            self._parent.rainbow_generator.pattern_duration = value
        except Exception as e:
            print(e)
            result = {
                "error": e.__dict__
            }
            # 422 Unprocessable Entity
            cherrypy.response.status = 422
        else:
            result = self._parent.rainbow_generator.pattern_duration
        return result


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
