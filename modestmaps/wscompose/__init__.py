# -*-python-*-

__version__    = "1.1"
__author__     = "Aaron Straup Cope"
__url__        = "http://www.aaronland.info/python/wscompose"
__date__       = "$Date: 2008/01/04 06:23:46 $"
__copyright__  = "Copyright (c) 2007-2008 Aaron Straup Cope. BSD license : http://www.modestmaps.com/license.txt"

import signal, thread, threading, time, sys
import BaseHTTPServer, SocketServer, mimetypes
import ModestMaps

from urlparse import urlparse
from cgi import parse_qs, escape
from math import sin, cos, acos, radians, degrees
import tempfile
import textwrap
import string
import StringIO
import types

import validate

# TO DO :
#
# - update to use wsgi

class handler(BaseHTTPServer.BaseHTTPRequestHandler):

    # ##########################################################
    
    def __init__ (self, request, client_address, server) :
        self.ctx = {}
        self.points = {}
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        
    # ##########################################################
    
    def do_GET (self):

        scheme, host, path, params, query, hash = urlparse(self.path)
        params = parse_qs(query)
        
        if not self.load_ctx(params) :
            return

        img = self.draw_map()
        self.send_map(img)

        return

    # ##########################################################

    def do_POST (self) :

        clen = self.headers.getheader('content-length')
        
        if clen:
            clen = int(clen)
        else:
            self.send_error(400, "Missing Content-Length parameter");
            return

        query = self.rfile.read(clen)
        params = parse_qs(query)

        if not self.load_ctx(params) :
            return

        img = self.draw_map()

        self.send_map(img)
        return
    
    # ##########################################################

    def load_ctx (self, params) :
        args = self.validate_params(params)
        
        if not args :
            return False

        self.ctx = args
        return True
    
    # ##########################################################
    
    def draw_map (self) :

        try :

            if self.ctx['method'] == 'extent' :
                return self.draw_map_extentified()
            elif self.ctx['method'] == 'bbox' :
                return self.draw_map_bbox()                
            else :
                return self.draw_map_centered()
            
        except Exception, e :
            self.error(200, "composer error : %s" % e)
            return False

    # ##########################################################
    
    def draw_map_extentified (self) :

        if self.ctx.has_key('adjust') :
            self.ctx['bbox'] = self.__adjust_bbox(self.ctx['bbox'], self.ctx['adjust'])
            
        #

        provider = self.load_provider(self.ctx['provider'])

        sw = ModestMaps.Geo.Location(self.ctx['bbox'][0], self.ctx['bbox'][1])
        ne = ModestMaps.Geo.Location(self.ctx['bbox'][2], self.ctx['bbox'][3])
        dims = ModestMaps.Core.Point(self.ctx['width'], self.ctx['height']);
        
        self.ctx['map'] = ModestMaps.mapByExtent(provider, sw, ne, dims)

        coord, offset = ModestMaps.calculateMapExtent(provider,
                                                      self.ctx['width'], self.ctx['height'],
                                                      ModestMaps.Geo.Location(self.ctx['bbox'][0], self.ctx['bbox'][1]),
                                                      ModestMaps.Geo.Location(self.ctx['bbox'][2], self.ctx['bbox'][3]))
        
        self.ctx['zoom'] = coord.zoom

        return self.ctx['map'].draw()
        
    # ##########################################################
    
    def draw_map_centered (self) :
        
        provider = self.load_provider(self.ctx['provider'])    

        loc = ModestMaps.Geo.Location(self.ctx['latitude'], self.ctx['longitude'])
        dim = ModestMaps.Core.Point(self.ctx['width'], self.ctx['height'])
        zoom = self.ctx['zoom']

        self.ctx['map'] = ModestMaps.mapByCenterZoom(provider, loc, zoom, dim)
        return self.ctx['map'].draw()
        
    # ##########################################################

    def draw_map_bbox (self) :

        if self.ctx.has_key('adjust') :
            self.ctx['bbox'] = self.__adjust_bbox(self.ctx['bbox'], self.ctx['adjust'])
        
        #

        provider = self.load_provider(self.ctx['provider'])

        sw = ModestMaps.Geo.Location(self.ctx['bbox'][0], self.ctx['bbox'][1])
        ne = ModestMaps.Geo.Location(self.ctx['bbox'][2], self.ctx['bbox'][3])
        zoom = self.ctx['zoom']

        self.ctx['map'] = ModestMaps.mapByExtentZoom(provider, sw, ne, zoom)
        return self.ctx['map'].draw()
        
    # ##########################################################
    
    def __adjust_bbox (self, bbox, adjust) :
        
        swlat = bbox[0]
        swlon = bbox[1]
        nelat = bbox[2]
        nelon = bbox[3]

        adjust_ne = 1
        adjust_sw = 1

        if nelon < 0 :
            adjust_ne = - adjust_ne

        if swlon < 0 :
            adjust_sw = - adjust_sw

        dist_n = self.__dist(nelat, nelon, nelat, (nelon + adjust_ne))
        dist_s = self.__dist(swlat, swlon, swlat, (swlon + adjust_sw))

        swlat = swlat - (float(adjust) / float(dist_s))
        swlon = swlon - (float(adjust) / float(dist_s))
        nelat = nelat + (float(adjust) / float(dist_n))
        nelon = nelon + (float(adjust) / float(dist_n))

        return [swlat, swlon, nelat, nelon]
    
    # ##########################################################

    def __dist(self, lat1, lon1, lat2, lon2) :

        theta = lon1 - lon2
        dist = sin(radians(lat1)) * sin(radians(lat2)) +  cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(theta));
        dist = acos(dist);
        dist = degrees(dist);

        return dist * 60        

    # ##########################################################
    
    def send_map (self, img) :

        if self.ctx['output'] == 'json' :
            return self.send_map_as_json(img)

        #
        
        format = self.ctx.get('output', 'png')
        
        fh = StringIO.StringIO()
        img.save(fh, format.upper())
        
        self.send_response(200, "OK")
        self.send_header("Content-Type", "image/%(format)s" % locals())
        self.send_header("Content-Length", fh.len)         

        self.send_x_headers(img)
        self.end_headers()

        self.wfile.write(fh.getvalue())
        return

    # ##########################################################

    def send_map_as_json (self, img) :

        js = self.generate_javascript_output(img)
        
        self.send_response(200, "OK")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(js))         

        self.send_x_headers(img)
        self.end_headers()

        self.wfile.write(js)
        return

    # ##########################################################

    def generate_javascript_output(self, img) :

        import base64
        
        fh = StringIO.StringIO()
        img.save(fh, "PNG")

        # this probably means it's time to
        # invest in a templating system...
        
        js = "{"

        js += "\"X-wscompose-Image-Height\":\"%s\"," % img.size[1]
        js += "\"X-wscompose-Image-Width\":\"%s\"," % img.size[0]
        js += "\"X-wscompose-Map-Zoom\":\"%s\"," % self.ctx['zoom']

        if self.ctx.has_key('plots') :
            for data in self.ctx['plots'] :

                pt = self.latlon_to_point(data['latitude'], data['longitude'])

                header = "X-wscompose-Plot-%s" % data['label']
                coords = "%s,%s" % (int(pt.x), int(pt.y))

                js += "\"%s\":\"%s\"," % (header, coords)

        js += "\"data\":\"%s\"" % base64.b64encode(fh.getvalue())
        js += "}"

        if self.ctx.has_key('json_callback') :
            js = "%s(%s)" % (self.ctx['json_callback'], js)

        return js
    
    # ##########################################################

    def send_x_headers (self, img) :
        self.send_header("X-wscompose-Image-Height", img.size[1])
        self.send_header("X-wscompose-Image-Width", img.size[0])        
        self.send_header("X-wscompose-Map-Zoom", self.ctx['zoom'])

        if self.ctx.has_key('plots') :
            for data in self.ctx['plots'] :

                pt = self.latlon_to_point(data['latitude'], data['longitude'])

                header = "X-wscompose-Plot-%s" % data['label']
                coords = "%s,%s" % (int(pt.x), int(pt.y))

                self.send_header(header, coords)
                
    # ##########################################################

    def latlon_to_point (self, lat, lon) :

        key = "%s-%s" % (lat, lon)

        if not self.points.has_key(key) :
            loc = ModestMaps.Geo.Location(lat, lon)
            pt = self.ctx['map'].locationPoint(loc)
            self.points[key] = pt

        return self.points[key]
    
    # ##########################################################
    
    def load_provider (self, value) :

	if value.startswith('http://'):
	    return ModestMaps.Providers.TemplatedMercatorProvider(value)
        elif value in ModestMaps.builtinProviders:
	    return ModestMaps.builtinProviders[value]()
        else :
            return None
            
    # ##########################################################
    
    def validate_params (self, params) :

        validator = validate.validate()
        
        if len(params.keys()) == 0 :
            self.help()
            return False

        #
        # I am a blank canvas
        #
        
        valid = {'output' : 'png'}

        #
        # La la la - I can't hear you
        #
        
        if not params.has_key('method') :
            params['method'] = ['center']
            

        #
        # Everyone needs a provider...
        #
        
        try :
            validator.ensure_args(params, ('provider',))
        except Exception, e :
            self.error(101, e)
            return False

        try :
            valid['provider'] = validator.provider(params['provider'][0])
        except Exception, e :
            self.error(101, e)
            return False
        
        #
        # Method specific requirements
        #
        
        if params['method'][0] == 'extent' :

            try :
                validator.ensure_args(params, ('bbox', 'height', 'width'))
            except Exception, e :
                self.error(111, e)
                return False

            try :
                valid['bbox'] = validator.bbox(params['bbox'][0])
            except Exception, e :
                self.error(112, e)
                return False

            for p in ('height', 'width') :

                try :
                    valid[p] = validator.dimension(params[p][0])
                except Exception, e :
                    self.error(113, e)
                    return False

            if params.has_key('adjust') :

                try :
                    valid['adjust'] = validator.bbox_adjustment(params['adjust'][0])
                except Exception, e :
                    self.error(124, e)
                    return False

            # you can blame migurski for this
            
            if params.has_key('zoom') :
                self.error(125, "'zoom' is not a valid argument when method is 'extent'")
                return False
                
        elif params['method'][0] == 'bbox' :

            try :
                validator.ensure_args(params, ('bbox', 'zoom'))
            except Exception, e :
                self.error(121, e)
                return False

            try :
                valid['bbox'] = validator.bbox(params['bbox'][0])
            except Exception, e :
                self.error(122, e)
                return False

            try :
                valid['zoom'] = validator.zoom(params['zoom'][0])
            except Exception, e :
                self.error(123, e)
                return False

            if params.has_key('adjust') :

                try :
                    valid['adjust'] = validator.bbox_adjustment(params['adjust'][0])
                except Exception, e :
                    self.error(124, e)
                    return False

            # you can blame migurski for this
            
            for p in ('height', 'width') :
                if params.has_key(p) :
                    self.error(125, "'%s' is not a valid argument when method is 'bbox'" % p)
                    return False
                
        # center
        
        else :

            try :
                validator.ensure_args(params, ('latitude', 'longitude', 'zoom', 'height', 'width'))
            except Exception, e :
                self.error(131, e)
                return False

            for p in ('latitude', 'longitude') :
        
                try :
                    valid[p] = validator.latlon(params[p][0])
                except Exception, e :
                    self.error(132, e)
                    return False

            try :
                valid['zoom'] = validator.zoom(params['zoom'][0])
            except Exception, e :
                self.error(133, e)
                return False

            for p in ('height', 'width') :

                try :
                    valid[p] = validator.dimension(params[p][0])
                except Exception, e :
                    self.error(134, e)
                    return False
            

        #
        # plotting or "headless" markers
        #

        if params.has_key('plot') :

            try :
                valid['plots'] = validator.plots(params['plot'])
            except Exception, e :
                self.error(141, e)
                return False

        #
        # json ?
        #

        if params.has_key('output') :

            out = params['output'][0].lower()
            
            if out == 'json' :
                valid['output'] = 'json'                

            elif out == 'javascript' :
                if not params.has_key('callback') :
                    self.error(142, 'Missing JSON callback')
                    return False
            
                try :
                    valid['json_callback'] = validator.json_callback(params['callback'][0])
                except Exception, e:
                    self.error(143, e)
                    return False

                valid['output'] = 'json'

            elif out in ('png', 'jpeg') :
                valid['output'] = out     
            
            else :
                self.error(144, 'Not a valid output format')
                return False
                
        #
        # whoooosh
        #

        valid['method'] = params['method'][0]

        return valid

    # ##########################################################

    # learn about python 'mixins' - it would nice to move this
    # into a separate package...
    
    # ##########################################################
    
    def help (self) :
        
        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        
        self.help_synopsis()
        self.help_example()
        self.help_parameters()
        self.help_metadata()        
        self.help_errors()
        self.help_notes()
        self.help_questions()
        self.help_license()

    # ##########################################################

    def help_synopsis (self) :
        self.help_para("ws-compose.py - a bare bone HTTP interface to the ModestMaps map tile composer.\n\n")
        
    # ##########################################################
    
    def help_example (self) :
        self.help_header("Example")
        self.help_para("http://127.0.0.1:9999/?provider=MICROSOFT_ROAD&latitude=41.904688&longitude=12.494308&zoom=17&height=500&width=500")
        self.help_para("Returns a PNG file of a map centered on the Santa Maria della Vittoria, in Rome.")
        
    # ##########################################################
    
    def help_parameters (self) :
        self.help_header("Parameters")
        self.help_option('provider', 'A valid ModestMaps map tile provider.', True)
        self.help_option('method', 'One of the following options :', True)

        self.help_option('center', 'Render map tiles centered around a specific coordinate. If defined, the following parameters must also be present : ', False, 1)
        self.help_option('latitude','A valid decimal latitude.', True, 2)
        self.help_option('longitude', 'A valid decimal longitude.', True, 2)
        self.help_option('accuracy', 'The zoom level / accuracy (as defined by ModestMaps rather than any individual tile provider) of the final image.', True, 2)
        self.help_option('height', 'The height of the final image', True, 2)
        self.help_option('width', 'The width of the final image', True, 2)

        self.help_option('extent', 'Render map tiles at a suitable zoom level in order to fit a bounding box in an image with specific dimensions. If defined, the following parameters must also be present : ', False, 1)
        self.help_option('bbox', 'A bounding box comprised of comma-separated decimal coordinates in the following order : SW latitude, SW longitude, NE latitude, NE longitude', True, 2)
        self.help_option('height', 'The height of the final image', True, 2)
        self.help_option('width', 'The width of the final image', True, 2)

        self.help_option('bbox', 'Render all the map tiles necessary to display a bounding box at a specific zoom level. If defined, the following parameters must also be present : ', False, 1)
        self.help_option('bbox', 'A bounding box comprised of comma-separated decimal coordinates in the following order : SW latitude, SW longitude, NE latitude, NE longitude', True, 2)
        self.help_option('accuracy', 'The zoom level / accuracy (as defined by ModestMaps rather than any individual tile provider) of the final image.', True, 2)

        self.help_option('output', 'Although the default output format for maps is \'png\' (you know, like a PNG image file) you may also specify the following alternatives: ', False)
        self.help_option('json', 'Return a Base64 encoded version of a PNG image, as well as any extra X-wscompose headers, as JSON data structure.', False, 1)        
        self.help_option('javascript', 'Return a Base64 encoded version of a PNG image, as well as any extra X-wscompose headers, as JSON data structure wrapped in a function whose name is defined by the \'callback\' parameter.', False, 1)        
        self.help_option('callback', 'Required if the output format is \'javascript\'; this is the name of the callback function that your JSON data structure will be wrapped in.', False)        

        self.help_option('plot', 'Plot -- but do not render -- the x and y coordinates for a given point. Coordinate data will be returned HTTP header(s) named \'X-wscompose-plot-\' followed by the label you choose when passing latitude and longitude information. You may pass multiple plot arguments, each of which should contain the following comma separated values :', False)
        self.help_option('label', 'A unique string to identify the plotting by', True, 1)
        self.help_option('point', 'A comma-separated string containing the latitude and longitude indicating the point to be plotted', True, 1)
        
    # ##########################################################

    def help_metadata (self) :
        self.help_header("Metadata")

        self.help_para("Metadata about an image is returned in HTTP headers prefixed with 'X-wscompose-'.")
        self.help_para("For example : ")
        
        self.help_pre("""	HTTP/1.x 200 OK
        Server: BaseHTTP/0.3 Python/2.5
        Date: Sun, 13 Jan 2008 01:08:37 GMT
        Content-Type: image/png
        Content-Length: 1946576
        X-wscompose-Image-Height: 1024
        X-wscompose-Image-Width: 1024
        X-wscompose-Map-Zoom: 14.0
        X-wscompose-plot-roy: 667,285""")

        self.help_para("Most headers are self-explanatory. Plotted coordinates are a little more complicated.")

        self.help_para("The string after 'X-wscompose-plot' is the label assigned to the marker when the API call was made. The value is a comma separated list containing the x and y coordinates for (label's) corresponding latitude and longitude.")
        
    # ##########################################################    

    def help_errors (self) :
        self.help_header("Errors")
        self.help_para("Errors are returned with the HTTP status code 500. Specific error codes and messages are returned both in the message body as XML and in the 'X-ErrorCode' and 'X-ErrorMessage' headers.") 
        
    # ##########################################################
        
    def help_notes (self) :
        # self.help_header("Notes")        
        return
    
    # ##########################################################
    
    def help_questions (self) :
        self.help_header("Questions")
        self.help_qa("Is it fast?", "Not really. It is designed, primarily, to be run on the same machine that is calling the interface.") 
        self.help_qa("Will it ever be fast?", "Sure. It is on The List (tm) to create a mod_python and/or wsgi version. Patches are welcome.")
        self.help_qa("Can I request map images asynchronously?", "Not yet.")
        self.help_qa("Can I get a pony?", "No.")
        
    # ##########################################################
    
    def help_license (self) :
        self.help_header("License")
        self.help_para("Copyright (c) 2007-2008 Aaron Straup Cope. All Rights Reserved. This is free software. You may redistribute it and/or modify it under the same terms the BSD license : http://www.modestmaps.com/license.txt")
        
    # ##########################################################
    
    def help_para(self, text) :

        self.wfile.write(textwrap.fill(text, 72))
        self.wfile.write("\n\n")

    # ##########################################################

    def help_pre (self, txt) :
        self.wfile.write(txt)
        self.wfile.write("\n\n")
        
    # ##########################################################
    
    
    def help_header (self, title) :
        ln = "-" * 72
        self.wfile.write("%s\n" % ln);
        self.wfile.write("%s\n" % title.upper())
        self.wfile.write("%s\n\n" % ln);

    # ##########################################################
    
    def help_option (self, opt, desc, required, indent=0) :

        indent_opt = "\t" * indent
        indent_desc = "\t" * (indent + 1)
        
        present = "required"

        if not required :
            present = "optional"

        opt = textwrap.fill("* %s (%s)" % (opt, present), 72, initial_indent=indent_opt, subsequent_indent=indent_opt)
        desc = textwrap.fill(desc, 72, initial_indent=indent_desc, subsequent_indent=indent_desc)
        
        self.wfile.write("%s\n\n%s\n\n" % (opt, desc))

    # ##########################################################
    
    def help_qa(self, question, answer) :
        self.wfile.write("%s\n\n" % question)
        self.wfile.write("%s\n\n" % textwrap.fill(answer, 72, initial_indent="\t", subsequent_indent="\t"))

    # ##########################################################
    
    def error (self, err_code=999, err_msg="OH NOES!!! INVISIBLE ERRORZ!!!") :

        err_code = self.sanitize(err_code)
        err_msg  = self.sanitize(err_msg)

        print "[%s] %s" % (err_code, err_msg)
        
        self.send_response(500, "Server Error")
        self.send_header("Content-Type", "application/xml") 
        self.send_header("X-ErrorCode", err_code)
        self.send_header("X-ErrorMessage", err_msg)         
        self.end_headers()
        self.wfile.write("<?xml version=\"1.0\" ?><error code=\"%s\">%s</error>" % (err_code, err_msg))

    # ##########################################################
    
    def sanitize (self, str) :
        return escape(unicode(str))

class _wwwserver(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

class server :

    def __init__ (self, handler, port=9999) :

        server = _wwwserver(("", port), handler)        
        server.allow_reuse_address = True
        
        self.__port__ = port
        self.__server__ = server
        self.__done__ = False
        
    def serve (self) :    
            signal.signal(signal.SIGINT, self.terminate)
            thread.start_new_thread(self.__server__.serve_forever,())
    
            while not self.__done__:
                try:
                    time.sleep(0.3)
                except IOError:
                    pass
   
            self.__server__.server_close()

    def terminate(self, sig_num, frame):
        self.__done__ = True    
    
    def loop (self):

        url = "http://127.0.0.1:%s" % self.__port__
        print "ws-compose derived server running on port %s" % self.__port__
        print "documentation and usage is available at %s/\n\n" % url

        self.serve()

if __name__ == "__main__ " :

    app = wscompose.server(wscompose.handler)
    app.loop()
