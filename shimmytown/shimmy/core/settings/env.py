# -*- coding: utf-8 -*-

from __future__ import absolute_import

# Standard Library
import json
import logging
from os import environ

logger = logging.getLogger()


def env_or(envvars, default, cast=str, **options):
    """
    Read an environment variable and return it or a default
    :param envvar: Varibale name. Name will be converted to uppercase
    :param default: default value if the variable is not set.
    :param type cast: type to cast the variable to. If the type is bool the envvar will be cast to an int first.
    :return: String of the variable.
    """
    if not envvars:
        return default

    if cast is bool:
        cast = lambda x: bool(int(x))  # flake8: noqa
    elif cast in (list, tuple):
        _cast = cast
        def cast(x):
            if isinstance(x, _cast):
                return x
            else:
                return _cast(_.strip() for _ in x.split(options.get('seperator', ',')))
    elif cast == 'json':
        def cast(x):
            return json.loads(x) if isinstance(x, str) else x

    if not isinstance(envvars, tuple):
        envvars = (envvars, )

    var = next(
        (
            environ.get(envvar, '')
            for envvar in map(str.upper, envvars)
            if envvar in environ
        ),
        default
    )

    return cast(var) if var is not None else None


def install_caps(g, l):
    """
    Update the globals() with all of the UPPERCASE_VARIABLES in locals()
    """
    g.update({k: v for k, v in l.items() if k.isupper()})


def log_setting(setting, message='is a thing', cache={}):
    if not IS_MAIN:
        if cache.setdefault('first', 1):
            logger.warning('----> Settings Info')
        logger.warning('  --> %-20s - %s', '[%s]' % setting, message)
        cache['first'] = 0


# RUN_MAIN will be set for the inner fork of a django debug env
RUN_MAIN = env_or('RUN_MAIN', None)
IS_MAIN = RUN_MAIN == 'true'

#: if true the environment is executing on a single host machine (os x or vagrant)
ENV_ENVIRONMENT = 'ENVIRONMENT'
ENVIRONMENT = env_or(ENV_ENVIRONMENT, '', str)
log_setting(ENVIRONMENT)

LOCAL = ENVIRONMENT == 'DEV'
LOCAL and log_setting('LOCAL', 'is enabled')

#: if true the environment is executing tests
TEST = ENVIRONMENT == 'TEST'
TEST and log_setting('TEST', 'is enabled')

#: if true the django debug options should be set
ENV_DEBUG = 'DEBUG'
DEBUG = env_or(ENV_DEBUG, False, bool)
DEBUG and log_setting('DEBUG', 'is enabled')

#: if true executing in a docker based environment
ENV_DOCKER = 'DOCKER'
DOCKER = env_or(ENV_DOCKER, False, bool)
DOCKER and log_setting('DOCKER', 'is enabled')

#: if true output extra startup information
ENV_VERBOSE = 'VERBOSE'
VERBOSE = env_or(ENV_VERBOSE, False, bool)
VERBOSE and log_setting('VERBOSE', 'is enabled')

#: path for the GEOIP databases
ENV_GEOIP_PATH = 'GEOIP_PATH'

#: Name of the city database
ENV_GEOIP_CITY = 'GEOIP_CITY'

ENV_STATSD_HOST = 'STATSD_HOST'
ENV_STATSD_PORT = 'STATSD_PORT'

ENV_DATABASE_URL = 'DATABASE_URL'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_or('SECRET_KEY', 'i am very secret')

#: The unique identifier for the application. eg. "9daa2797-e49b-4624-932f-ec3f9688e3da"
HEROKU_APP_ID = env_or('HEROKU_APP_ID', None)

#: The application name. eg. "example-app"
HEROKU_APP_NAME = env_or('HEROKU_APP_NAME', None)

#: The dyno identifier. eg. "1vac4117-c29f-4312-521e-ba4d8638c1ac"
HEROKU_DYNO_ID = env_or('HEROKU_DYNO_ID', None)

#: The identifier for the current release. eg. "v42"
HEROKU_SLUG_ID = env_or('HEROKU_SLUG_ID', None)

#: The commit hash for the current release. eg. "2c3a0b24069af49b3de35b8e8c26765c1dba9ff0"
HEROKU_SLUG_COMMIT = env_or('HEROKU_SLUG_COMMIT', None)

#: The time and date the release was created. eg. "2015/04/02 18:00:42"
HEROKU_RELEASE_CREATED_AT = env_or('HEROKU_RELEASE_CREATED_AT', None)

#: The description of the current release. eg. "Deploy 2c3a0b2"
HEROKU_RELEASE_DESCRIPTION = env_or('HEROKU_RELEASE_DESCRIPTION', None)

# Heroku bucketeer for aws bucket of static uploads, i.e. profile photos.
BUCKETEER_AWS_ACCESS_KEY_ID = env_or('BUCKETEER_AWS_ACCESS_KEY_ID', None)
BUCKETEER_AWS_SECRET_ACCESS_KEY = env_or('BUCKETEER_AWS_SECRET_ACCESS_KEY', None)
BUCKETEER_BUCKET_NAME = env_or('BUCKETEER_BUCKET_NAME', '')


SLACK_TOKEN = env_or('SLACK_TOKEN', None)
SLACK_FAIL_SILENTLY = env_or('SLACK_FAIL_SILENTLY', True)
SLACK_ICON_URL = env_or('SLACK_ICON_URL', '')
SLACK_BACKEND = env_or('SLACK_BACKEND', 'django_slack.backends.RequestsBackend')

PAYPAL_MODE = env_or('PAYPAL_MODE', 'sandbox')
PAYPAL_CLIENT_ID = env_or('PAYPAL_CLIENT_ID', None)
PAYPAL_CLIENT_SECRET = env_or('PAYPAL_CLIENT_SECRET', None)
