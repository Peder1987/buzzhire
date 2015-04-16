from geopy.geocoders.googlev3 import GoogleV3
from geopy.exc import GeopyError
from django.conf import settings
from django.contrib.gis import geos


class GeoLocationMatchException(Exception):
    """Exception for raising when there's an issue matching a location
    from user input."""
    pass


class GeoLocation(object):
    """A location on the planet.  Initialised using a user-submitted string,
    which it will attempt to process.  Raises a GeoLocationMatchException
    on failure.
    
    Once instantiated, will have two attributes:
    
        human_location: the human readable string of the matched location
        point: a GEOSGeometry object of the location
    """

    def __init__(self, location_string):

        geocoder = GoogleV3(api_key=settings.GOOGLE_API_SERVER_KEY)
        try:
            # Get location, restricted to uk
            location = geocoder.geocode(location_string, region='uk',
                                        components={'country': 'uk'})
            # If the location isn't matched, it will be None
            assert location
        except (GeopyError, AssertionError) as e:
            # This can happen for various reasons, but most likely
            # it will be an exceeded quota rather than a failure to match
            # the location - the API usually returns some kind of location
            raise GeoLocationMatchException
        else:
            # Build useful attributes on the object
            self.human_location, latlon = location
            # NB we need to reverse the order of latitude and longitude
            latitude, longitude = latlon
            self.point = geos.fromstr("POINT(%s %s)" % (longitude, latitude))

    def __repr__(self):
        return "<GeoLocation: %s>" % self.human_location
