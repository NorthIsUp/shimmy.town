#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

# Standard Library
import os
import sys
import time
from logging import getLogger

# No imports from lindy.* allowed, they will break settings setup

if __name__ == '__main__':
    logger = getLogger()

    try:
        import dotenv
        with open('.env') as dot_env:
            env = dotenv.parse_dotenv(dot_env.read())

            # log any updates to the environment
            logger.warning('----> Overrides from .env')
            pad = max(len(_) for _ in os.environ) + 2
            if env:
                for k, v in sorted(env.items()):
                    v = os.environ.setdefault(k, v)
                    logger.warning('  --> {k:·<{pad}} {v}'.format(pad=pad, k=k, v=v))
            else:
                logger.warning('  --> no overrides from .env')

    except (ImportError, FileNotFoundError):
        pass

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and not os.environ.get('DATABASE_AWS_CHECK'):
        if 'localhost' not in DATABASE_URL:
            logger.critical(' USING PRODUCTION DATABASE '.center(80, '-'))
            logger.critical(DATABASE_URL)
            logger.critical(' USING PRODUCTION DATABASE '.center(80, '-'))
            time.sleep(5)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
