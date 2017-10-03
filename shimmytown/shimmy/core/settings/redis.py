from __future__ import absolute_import

# External Libraries
import dj_redis_url

def patch_redis(g):
    g.setdefault('REDIS', {}).setdefault('')
    g['REDIS'] = {"default": dj_redis_url.config()}

