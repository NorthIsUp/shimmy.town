# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .env import (
    env_or,
    install_caps,
    log_setting,
)


def patch_email(g):
    g['SENDGRID_API_KEY'] = env_or('SENDGRID_API_KEY', None)

    if g['SENDGRID_API_KEY']:
        EMAIL_BACKEND = 'sgbackend.SendGridBackend'
    else:
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    log_setting('EMAIL_BACKEND', EMAIL_BACKEND)

    install_caps(g, locals())
