# vim:et sts=4 sw=4:

import sys, math, optparse, ModestMaps

class BadComposure(Exception):
    pass

parser = optparse.OptionParser(usage="""compose.py [options] file

There are three ways to set a map coverage area.

1) Center, zoom, and dimensions: create a map of the specified size,
   centered on a given geographical point at a given zoom level:

   python compose.py -p OPENSTREETMAP -d 800 800 -c 37.8 -122.3 -z 11 out.jpg

2) Extent and dimensions: create a map of the specified size that
   adequately covers the given geographical extent:

   python compose.py -p MICROSOFT_ROAD -d 800 800 -e 36.9 -123.5 38.9 -121.2 out.png

3) Extent and zoom: create a map at the given zoom level that covers
   the precise geographical extent, at whatever pixel size is necessary:
   
   python compose.py -p BLUE_MARBLE -e 36.9 -123.5 38.9 -121.2 -z 9 out.jpg""")

parser.add_option('-v', '--verbose', dest='verbose',
                  help='Make a bunch of noise',
                  action='store_true')

parser.add_option('-c', '--center', dest='center', nargs=2,
                  help='Center. lat, lon, e.g.: 37.804 -122.263', type='float',
                  action='store')

parser.add_option('-e', '--extent', dest='extent', nargs=4,
                  help='Geographical extent. Two lat, lon pairs', type='float',
                  action='store')

parser.add_option('-z', '--zoom', dest='zoom',
                  help='Zoom level', type='int',
                  action='store')

parser.add_option('-d', '--dimensions', dest='dimensions', nargs=2,
                  help='Pixel dimensions of image', type='int',
                  action='store')

parser.add_option('-p', '--provider', dest='provider',
                  help='Map Provider, one of ' + ', '.join(ModestMaps.builtinProviders.keys()) + ' or URL template like "http://example.com/{Z}/{X}/{Y}.png".',
                  action='store')

parser.add_option('-k', '--apikey', dest='apikey',
                  help='API key for map providers that need one, e.g. CloudMade', type='str',
                  action='store')

parser.add_option('-f', '--fat-bits', dest='fatbits',
                  help='Optionally look to lower zoom levels if tiles at the requested level are unavailable',
                  action='store_true')

if __name__ == '__main__':

    (options, args) = parser.parse_args()
    
    try:
        try:
            outfile = args[0]
        except IndexError:
            raise BadComposure('Error: Missing output file.')
        
        try:
            if options.provider.startswith('CLOUDMADE_'):
                if not options.apikey:
                    raise BadComposure("Error: Cloudmade provider requires an API key. Register at http://developers.cloudmade.com/")

                provider = ModestMaps.builtinProviders[options.provider](options.apikey)
            elif options.provider.startswith('http://'):
                provider = ModestMaps.Providers.TemplatedMercatorProvider(options.provider)
            elif options.provider.startswith('https://'):
                provider = ModestMaps.Providers.TemplatedMercatorProvider(options.provider)
            elif options.provider.startswith('file://'):
                provider = ModestMaps.Providers.TemplatedMercatorProvider(options.provider)
            else:
                provider = ModestMaps.builtinProviders[options.provider]()
        except KeyError:
            raise BadComposure('Error: bad provider "%s".' % options.provider)
    
        if options.center and options.extent:
            raise BadComposure("Error: bad map coverage, center and extent can't both be set.")
        
        elif options.extent and options.dimensions and options.zoom:
            raise BadComposure("Error: bad map coverage, dimensions and zoom can't be set together with extent.")
        
        elif options.center and options.zoom and options.dimensions:
            lat, lon = options.center[0], options.center[1]
            width, height = options.dimensions[0], options.dimensions[1]

            dimensions = ModestMaps.Core.Point(width, height)
            center = ModestMaps.Geo.Location(lat, lon)
            zoom = options.zoom

            map = ModestMaps.mapByCenterZoom(provider, center, zoom, dimensions)
            
        elif options.extent and options.dimensions:
            latA, lonA = options.extent[0], options.extent[1]
            latB, lonB = options.extent[2], options.extent[3]
            width, height = options.dimensions[0], options.dimensions[1]

            dimensions = ModestMaps.Core.Point(width, height)
            locationA = ModestMaps.Geo.Location(latA, lonA)
            locationB = ModestMaps.Geo.Location(latB, lonB)

            map = ModestMaps.mapByExtent(provider, locationA, locationB, dimensions)
    
        elif options.extent and options.zoom:
            latA, lonA = options.extent[0], options.extent[1]
            latB, lonB = options.extent[2], options.extent[3]

            locationA = ModestMaps.Geo.Location(latA, lonA)
            locationB = ModestMaps.Geo.Location(latB, lonB)
            zoom = options.zoom

            map = ModestMaps.mapByExtentZoom(provider, locationA, locationB, zoom)
    
        else:
            raise BadComposure("Error: not really sure what's going on.")

    except BadComposure, e:
        print >> sys.stderr, parser.usage
        print >> sys.stderr, ''
        print >> sys.stderr, '%s --help for possible options.' % __file__
        print >> sys.stderr, ''
        print >> sys.stderr, e
        sys.exit(1)

    if options.verbose:
        print map.coordinate, map.offset, '->', outfile, (map.dimensions.x, map.dimensions.y)

    map.draw(options.verbose, options.fatbits).save(outfile)
