from __future__ import absolute_import


def patch_all(g):
    from .email import patch_email
    patch_email(g)

    from .pipeline import patch_pipeline
    patch_pipeline(g)

    from .django import patch_django
    patch_django(g)

    from .redis import patch_redis
    patch_redis(g)

    from .storages import patch_storages
    patch_storages(g)
