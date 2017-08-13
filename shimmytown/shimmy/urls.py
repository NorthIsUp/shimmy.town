from django.conf.urls import url
from django.views.generic.base import RedirectView

from danceschool.core.classreg import StudentInfoView

from .forms import BLHContactForm
from .views import QuerysetAsCSVView, MNPEntryListView

urlpatterns = [
    # These are redirects to address old bookmarks/backlinks
    url(r'^classes/$', RedirectView.as_view(url='/register/',permanent=True)),
    url(r'^admin/classes/$', RedirectView.as_view(url='/register/',permanent=True)),
    url(r'^classes/id/(?P<marketing_id>[\w\-_]+)/$', RedirectView.as_view(url='/register/',permanent=True)),
    url(r'^classes/referral/(?P<voucher_id>[\w\-_]+)/$', RedirectView.as_view(url='/register/',permanent=True)),

    url(r'^policies.html$', RedirectView.as_view(url='/policies',permanent=True)),
    url(r'^policies/conduct/$', RedirectView.as_view(url='/policies#conduct',permanent=True)),
    url(r'^aboutus/$', RedirectView.as_view(url='/instructors',permanent=True)),
    url(r'^aboutus/retired/$', RedirectView.as_view(url='/instructors/retired',permanent=True)),
    url(r'^multimedia/$', RedirectView.as_view(url='/music',permanent=True)),

    # These views are just redirects because of changed URLs
    url(r'^gift_certificates/$', RedirectView.as_view(url='/gift-certificates',permanent=True)),

    # This should override the existing student info view to use our custom form.
    url(r'^register/getinfo/$', StudentInfoView.as_view(form_class=BLHContactForm), name='getStudentInfo'),

    # This is for the MNP Entry List
    url(r'^admin/mnp-list/$',MNPEntryListView.as_view(),name='MNPEntryList'),

    # This is for our custom DB query functionality
    url(r'^admin/submitquery/$',QuerysetAsCSVView.as_view(),name='submitquery'),
]
