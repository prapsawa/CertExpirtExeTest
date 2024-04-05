##########################################################################
#
# Copyright (c) 2024 by Cisco Systems, Inc.
# FileName: ServerResponseHandler
# Description: HTTPS Status Code Handler class to handle below codes:
#   1) 200 - OK [the request was processed and may or may not be fully
#                accepted - see response for details]
#   2) 202 - Accepted [the request was accepted and placed in a queue
#                      and processed asynchronously]
#   3) 400 - Bad Request [the request was rejected due to input errors ]
#   4) 401 - Unauthorized [the request was rejected due to an authorization
#                          error (e.g. the API key is invalid)]
#   5) 403 - Request Forbidden [the request was forbidden - user does not
#                               have authorization to access method]
#   6) 404 - Request Not Found [the request method is not available]
#   7) 405 - Method not allowed [the request method is not allowed]
#   8) 500 - Internal Server Error [the request failed due to an
#                                   unexpected server error]
#   9) 502 - Bad Gateway [the request failed due to bad gateway]
#   10) 503 - Service Unavailable [the request failed due to the service
#                                  being temporarily unavailable]
#   11) 504 - Gateway Timeout [the request failed due to gateway timeout]
#
###########################################################################
"""ServerResponseHandler Class"""

import logging


class ServerResponseHandler:
    @staticmethod
    def ServerResponseHandlerMethod(http_response):
        if http_response.status_code == 200:
            response = 'HTTP response code is 200 OK'
            logging.info(response)
            return True, response
        elif http_response.status_code == 202:
            response = 'HTTP response code is 202 Accepted'
            logging.info(response)
            return True, response
        elif http_response.status_code == 400:
            response = 'HTTP response code is 400 Bad Request'
            logging.info(response)
            return False, response
        elif http_response.status_code == 401:
            response = 'HTTP response code is 401 Unauthorized'
            logging.info(response)
            return False, response
        elif http_response.status_code == 403:
            response = 'HTTP response code is 403 Request Forbidden'
            logging.info(response)
            return False, response
        elif http_response.status_code == 404:
            response = 'HTTP response code is 404 Request Not Found'
            logging.info(response)
            return False, response
        elif http_response.status_code == 405:
            response = 'HTTP response code is 405 Method not allowed'
            logging.info(response)
            return False, response
        elif http_response.status_code == 500:
            response = 'HTTP response code is 500 Internal Server Error'
            logging.info(response)
            return False, response
        elif http_response.status_code == 502:
            response = 'HTTP response code is 502 Bad Gateway'
            logging.info(response)
            return False, response
        elif http_response.status_code == 503:
            response = 'HTTP response code is 503 Service Unavailable'
            logging.info(response)
            return False, response
        elif http_response.status_code == 504:
            response = 'HTTP response code is 504 Gateway Timeout'
            logging.info(response)
            return False, response
        else:
            response = f'HTTP response code is {http_response}'
            logging.info(response)
            return False, response
