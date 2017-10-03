# -*- coding: utf-8 -*-
from __future__ import absolute_import

# External Libraries
from pipeline.storage import (
    GZIPMixin,
    PipelineCachedStorage,
)
from storages.backends.s3boto import S3BotoStorage


StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')


class GZIPPipelineCachedStorage(GZIPMixin, PipelineCachedStorage):
    pass
