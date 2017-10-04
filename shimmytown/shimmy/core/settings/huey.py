# -*- coding: utf-8 -*-
from __future__ import absolute_import

# External Libraries
from shimmy.core.settings import env


def patch_huey(g):
    from huey import RedisHuey
    from redis import ConnectionPool

    pool = ConnectionPool.from_url(env.REDIS_URL)
    g['HUEY'] = RedisHuey('danceschool', connection_pool=pool)
