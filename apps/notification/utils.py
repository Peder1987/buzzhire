import json, httplib
import logging
from django.conf import settings


logger = logging.getLogger('project')


class ParseConnection(object):
    """Object for handling push requests via Parse.
    """
    PARSE_URL = 'api.parse.com'
    PARSE_PORT = 443
    PARSE_PUSH_ENDPOINT = '/1/push'


    def __init__(self):
        try:
            self.connection = httplib.HTTPSConnection(self.PARSE_URL,
                                                      self.PARSE_PORT)
            self.connection.connect()
        except Exception as e:
            logger.exception(e)


    def push_message(self, message, user, category,
                     content_type_name, object_id):
        data = {
           "where": {
             # The user email is used to identify the user
             # TODO - this should really be the user id, in case they change
             # their email address
             "userEmail": user.email,
           },
           "data": {
             "alert": message,
             "category": category,
             "content_type": content_type_name,
             "object_id": object_id,
           }
        }
        logger.debug('Attempting to send push notification: %s' % data)
        try:
            self.connection.request('POST', self.PARSE_PUSH_ENDPOINT,
                                    json.dumps(data), {
                   "X-Parse-Application-Id": settings.PARSE_APPLICATION_ID,
                   "X-Parse-REST-API-Key": settings.PARSE_REST_API_KEY,
                   "Content-Type": "application/json"
                 })
        except Exception as e:
            logger.debug('Push failed.')
            logger.exception(e)
        else:
            logger.debug('Push sent.')
