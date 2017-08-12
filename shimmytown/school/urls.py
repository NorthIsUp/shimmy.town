
"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import absolute_import

# External Libraries
from django.conf import settings
from django.conf.urls import (
    include,
    url,
)
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

urlpatterns += [
    # Include your own app's URLs first to override default app URLs
    # url(r'^', include('<yourapp>.urls')),
    # Now, include default app URLs
    url(r'^', include('danceschool.urls')),
    url(r'^_bootstrap', TemplateView.as_view(template_name='bootstrap.html')),
    url(r'^', include('cms.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
