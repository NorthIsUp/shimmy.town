# -*- coding: utf-8 -*-
from __future__ import absolute_import

# External Libraries
from django import http
from django.utils.deprecation import MiddlewareMixin


class NoWWWRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host()
        if host.startswith('www.'):
            if request.method == 'GET':  # if wanna be a prefect REST citizen, consider HEAD and OPTIONS here as well
                no_www_host = host[4:]
                url = request.build_absolute_uri().replace(host, no_www_host, 1)
                return http.HttpResponsePermanentRedirect(url)
