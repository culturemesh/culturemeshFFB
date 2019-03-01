#
# CultureMesh API Client
#
# Heavily based out of this: https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/exceptions.py

""" Defines exceptions thrown by the CultureMesh API client """

class ApiError(Exception):
    """Represents an exception returned by the remote API."""
    def __init__(self, status, message=None):
        self.status = status
        self.message = message

    def __str__(self):
        if self.message is None:
            return self.status
        else:
            return "%s (%s)" % (self.status, self.message)

class Timeout(Exception):
    """The request timed out."""
    pass
    
class HTTPError(TransportError):
    """An unexpected HTTP error occurred."""
    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return "HTTP Error: %d" % self.status_code

# TODO: add more.