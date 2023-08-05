from __future__ import unicode_literals

import requests
try:
    from httplib import (
        OK, CREATED, FORBIDDEN, UNAUTHORIZED, NOT_FOUND, UNPROCESSABLE_ENTITY, BAD_REQUEST,
        SERVICE_UNAVAILABLE, INTERNAL_SERVER_ERROR, METHOD_NOT_ALLOWED, )
except ImportError:
    from http.client import (
        OK, CREATED, FORBIDDEN, UNAUTHORIZED, NOT_FOUND, UNPROCESSABLE_ENTITY, BAD_REQUEST,
        SERVICE_UNAVAILABLE, INTERNAL_SERVER_ERROR, METHOD_NOT_ALLOWED, )

import logging


logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    pass


class ServiceError(Exception):
    pass


class InvalidDataError(Exception):
    def __init__(self, message, errors):
        self.errors = errors
        self.message = message


class FiftyThreeClient(object):
    def __init__(
            self, api_key, endpoint=None, source_url=None, api_version='v2',
            use_secure=True):
        self.api_key = api_key
        self.endpoint = endpoint or 'fiftythree.organize.org'
        # self.api_version = api_version
        self.source_url = source_url or 'https://register.organize.org/'
        self.use_secure = use_secure
        if use_secure:
            self.scheme = 'https://'
        else:
            self.scheme = 'http://'
        self.lookup_zipcode_path = '/api/{}/postal-codes/'.format(api_version)
        self.submit_email_path = '/api/{}/emails/'.format(api_version)
        self.register_path = '/api/{}/registrations/'.format(api_version)
        self.revoke_path = '/api/{}/revocations/'.format(api_version)
        self.email_next_of_kin_path = '/api/{}/next-of-kin-emails/'.format(api_version)

    @property
    def _headers(self):
        return {
            'Authorization': 'Token {}'.format(self.api_key),
        }

    def lookup_zipcode_api_path(self, api_version):
        self.lookup_zipcode_path = '/api/{}/postal-codes/'.format(api_version)

    def submit_email_api_path(self, api_version):
        self.submit_email_path = '/api/{}/emails/'.format(api_version)

    def register_api_path(self, api_version):
        self.register_path = '/api/{}/registrations/'.format(api_version)

    def revoke_api_path(self, api_version):
        self.revoke_path = '/api/{}/revocations/'.format(api_version)

    def email_next_of_kin_api_path(self, api_version):
        self.email_next_of_kin_path = '/api/{}/next-of-kin-emails/'.format(api_version)

    def lookup_postal_code(self, postal_code):
        url = ''.join(
            [self.scheme, self.endpoint, self.lookup_zipcode_path,
             unicode(postal_code), '/', ])
        try:
            r = requests.get(url, headers=self._headers)
        except requests.ConnectionError as e:
            logger.error(e)
            raise ServiceError('Service unavailable.')

        if r.status_code == OK:
            return r.json()

        elif r.status_code in (UNAUTHORIZED, FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == NOT_FOUND:
            raise InvalidDataError(
                'Invalid postal code.',
                {'postal_code': ['Invalid postal code.']})

        elif r.status_code == UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                SERVICE_UNAVAILABLE, INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def submit_email(self, **data):
        url = ''.join([self.scheme, self.endpoint, self.submit_email_path, ])

        try:
            r = requests.post(url, headers=self._headers, data=data)
        except requests.ConnectionError as e:
            logger.error(e)
            raise ServiceError('Service unavailable.')

        if r.status_code == OK:
            return True

        elif r.status_code == CREATED:
            logger.info('Successfully submitted email')

        elif r.status_code in (UNAUTHORIZED, FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                SERVICE_UNAVAILABLE, INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def register(self, **data):
        url = ''.join([self.scheme, self.endpoint, self.register_path, ])
        data['source_url'] = self.source_url

        r = requests.post(url, headers=self._headers, data=data)

        if r.status_code == OK:
            return None

        elif r.status_code in (METHOD_NOT_ALLOWED, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code in (UNAUTHORIZED, FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                SERVICE_UNAVAILABLE, INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        elif r.status_code == CREATED:
            logger.info('Successfully submitted registration')
            # get the uuid and return it
            return r.json()['uuid']

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return None

    def revoke(self, **data):
        url = ''.join([self.scheme, self.endpoint, self.revoke_path, ])
        data['source_url'] = self.source_url

        r = requests.post(url, headers=self._headers, data=data)

        if r.status_code == OK:
            return r.json

        elif r.status_code in (METHOD_NOT_ALLOWED, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code in (UNAUTHORIZED, FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                SERVICE_UNAVAILABLE, INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        elif r.status_code == CREATED:
            logger.info('Successfully submitted revocation')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def email_next_of_kin(self, **data):
        url = ''.join([self.scheme, self.endpoint, self.email_next_of_kin_path, ])

        r = requests.post(url, headers=self._headers, data=data)

        if r.status_code == OK:
            return r.json()

        elif r.status_code in (METHOD_NOT_ALLOWED, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code in (UNAUTHORIZED, FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                SERVICE_UNAVAILABLE, INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        elif r.status_code == CREATED:
            logger.info('Successfully submitted next of kin email')
            return r.json()

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def document(self, name):
        url = ''.join(
            [self.scheme, self.endpoint, '/api/v2/', name, '/'])
        try:
            r = requests.get(url, headers=self._headers)
        except requests.ConnectionError as e:
            logger.error(e)
            raise ServiceError('Service unavailable.')

        if r.status_code == OK:
            return r.json()

        elif r.status_code in (UNAUTHORIZED, FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == NOT_FOUND:
            raise InvalidDataError('No Document Available.', {})

        elif r.status_code == UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                SERVICE_UNAVAILABLE, INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False
