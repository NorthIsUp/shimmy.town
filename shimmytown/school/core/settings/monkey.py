def patch_all(g):
    from .email import patch_email

    patch_email(g)
