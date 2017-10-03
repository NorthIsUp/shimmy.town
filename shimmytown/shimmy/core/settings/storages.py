# -*- coding: utf-8 -*-

from __future__ import absolute_import

def patch_storages(g):
    g['AWS_S3_OBJECT_PARAMETERS'] = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }
