# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.http import StreamingHttpResponse
from django.views.generic import FormView, TemplateView
from django.apps import apps
from django.db.models import Q
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError

import csv
import re
import six
from datetime import datetime, timedelta
from braces.views import PermissionRequiredMixin, UserFormKwargsMixin

from danceschool.core.models import Customer, StaffMember

from .forms import QuerysetForm

if six.PY3:
    # Ensures that checks for Unicode data types (and unicode type assignments) do not break.
    unicode = str


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class MNPEntryListView(PermissionRequiredMixin, TemplateView):
    template_name = 'shimmy/mnp_entry_list.html'
    permission_required = 'shimmy.run_database_query'

    def get_context_data(self,**kwargs):
        context = super(MNPEntryListView, self).get_context_data(**kwargs)

        set_time = kwargs.get('datetime', datetime.now())

        customers = Customer.objects.filter(
            registration__eventregistration__event__eventoccurrence__startTime__range=(
                set_time.date() - timedelta(days=set_time.weekday()),set_time.date() - timedelta(days=set_time.weekday() - 7)),
            registration__eventregistration__event__series__special=False,
        ).distinct().order_by('first_name','user__first_name')

        staffMembers = StaffMember.objects.filter(
            Q(instructor__status='R') |
            Q(eventstaffmember__event__month=set_time.month,eventstaffmember__event__year=set_time.year)
        ).distinct().order_by('firstName','userAccount__first_name')

        context.update({
            'customers': customers,
            'staffMembers': staffMembers,
            'thisMonday': set_time.date() - timedelta(days=set_time.weekday()),
        })

        return context


class QuerysetAsCSVView(PermissionRequiredMixin, UserFormKwargsMixin, FormView):
    form_class = QuerysetForm
    template_name = 'cms/forms/display_form_classbased_admin.html'
    permission_required = 'shimmy.run_database_query'

    def get_context_data(self,**kwargs):
        context = super(QuerysetAsCSVView,self).get_context_data(**kwargs)
        context.update({
            'form_title': 'Query the Site Database',
        })
        return context

    # Process the results
    def form_valid(self, form):
        from itertools import chain

        # These are the builtins that are allowed to be used in eval calls.
        builtins_whitelist = {
            'True': True,
            'False': False,
            'None': None,
        }

        if form.cleaned_data['existingQuery']:
            model_string = form.cleaned_data['existingQuery'].model
            qs_string = form.cleaned_data['existingQuery'].query
            fields = form.cleaned_data['existingQuery'].fields
        else:
            model_string = form.cleaned_data['model']
            qs_string = form.cleaned_data['queryset']
            fields = form.cleaned_data['fields']

        if fields:
            fields_list = fields.replace('\r','').split('\n')
        else:
            fields_list = []

        this_model_name = model_string.split('.')[-1]
        this_model = apps.get_model(model_string)
        new_queryset_string = qs_string.replace(this_model_name,'this_model',1)

        # Evaluate the queryset in a sandbox here
        qs = eval(
            new_queryset_string,{
                '__builtins__':builtins_whitelist,
                'this_model':this_model,
                'datetime': datetime,
                'timedelta': timedelta,
                'now': datetime.now(),
                'Q': Q,
            })

        if not type(qs) is QuerySet:
            raise ValidationError('Queryset is not valid.')

        model = this_model

        # Start the Http Stream, then generate through to write to it.
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer, csv.excel)

        # This function is called for each row in the returned queryset
        def getRow(obj,to_parse=[]):
            row = []

            if not to_parse:
                for field in headers:
                    val = getattr(obj, field)
                    if callable(val):
                        val = val()
                    if type(val) == list:
                        val = '\r\n'.join(val)
                    if type(val) is bytes:
                        val = val.decode("utf-8")
                    row.append(val)
            else:
                for field in to_parse:
                    try:
                        val = eval('obj.%s' % field,{
                            '__builtins__':builtins_whitelist,
                            'datetime': datetime,
                            'timedelta': timedelta,
                            'now': datetime.now(),
                            'Q': Q,
                            'obj': obj,
                        })
                    except:
                        val = ''

                    if type(val) == list:
                        val = '\r\n'.join(val)
                    if type(val) is bytes:
                        val = val.decode("utf-8")
                    row.append(val)
            return row

        to_parse = []

        # Define the header rows automatically or manually
        if not fields_list:
            headers = []
            for field in model._meta.fields:
                if 'password' not in field.name:
                    headers.append(field.name)
        else:
            # Separate out headers, then split out subarguments (foreign keys) and
            # passed arguments to callables
            equals_split = [re.split(r"=+(?=[^()]*(?:\(|$))", field) for field in fields_list]
            headers = [x[0].strip("'\"") for x in equals_split]
            to_parse = ['='.join(x).replace(x[0] + '=','',1) for x in equals_split]

        # Chain the generators together to add header rows
        output_data = chain(
            (writer.writerow(x) for x in [headers,]),
            (writer.writerow(getRow(obj,to_parse)) for obj in qs))

        response = StreamingHttpResponse(
            output_data,
            content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="querysetResults.csv"'
        return response
