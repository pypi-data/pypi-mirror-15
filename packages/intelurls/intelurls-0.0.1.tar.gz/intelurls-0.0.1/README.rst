=================
Intel URL Parsing
=================

This module started as a simple parser for Intel URLs for Niantic Lab's
Ingress game.  It then grew, like an ugly monster, to support most flavors
of Google Maps and Apple Maps URLs.

When a URL is parsed, we return a structure that contains the latitude and
longitude of the place, along with a host of other values, such as a name
for the map, potential zoom levels for the map, and human captions if we
can decipher them from the map service provider.

See the source code for the exact return values.

Niantic Labs is not responsible for this program, and neither endorses
nor supports it.  The author is not associated with Niantic Labs and
makes no representations.

Use
---

::
    >>> from intelurls import check_mapurl, parse_mapurl, parse_natural
    >>> check_mapurl("this is a string with a url in it https://www.ingress.com/intel?ll=37.821523,-122.377385&z=17 and more test")
    'https://www.ingress.com/intel?ll=37.821523,-122.377385&z=17'
    >>> parse_mapurl("https://maps.google.com/maps?ll=37.765727,-122.431961&cid=10889150637731333995&q=Beck's%20Motor%20Lodge")
    {'latlng': [37.765727, -122.431961], 'caption': "Beck's Motor Lodge", 'name': 'map_@37.765727,-122.431961'}
    >>> parse_mapurl("http://goo.gl/maps/r6T6a")
    {'latlng': [45.0215057, 14.6293757], 'caption': '', 'name': 'map_@45.0215057,14.6293757'}
    >>> parse_natural("San Francisco, CA")
    {'latlng': [37.7749295, -122.4194155], 'zoom': 13, 'caption': 'San Francisco, CA, USA', 'name': 'map_@37.7749295,-122.4194155_z13'}


Testing
-------

There are so many combinations of URLs, and the code is so hairy, that a
regression test jig was created.  However, since it is regression testing
based upon live data returned from service providers (in the case of some
of the more complex URLs and natural language processing), it is possible
for the `valid.out` data that was created using `gentest.py` to get out
of date.

If that happens, take a peek at the data differences and see if they are
legitimate (this code is broken) or the third party service has just changed
things a bit.  If you need to, you can regenerate valid.out.

A failed test isn't a reason to not install the module.
