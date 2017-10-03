from __future__ import absolute_import

# External Libraries
from crispy_forms.bootstrap import Alert
from crispy_forms.layout import (
    Div,
    Layout,
)
from danceschool.core.forms import RegistrationContactForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .core.constants import HOW_HEARD_CHOICES
from .helpers import get_model_choices
from .models import DatabaseQuery


class BLHContactForm(RegistrationContactForm):
    '''
    This is the BLH-specific form that customers use to fill out their contact info.
    It inherits from the danceschool app's basic form.
    '''

    agreeToPolicies = forms.BooleanField(required=True,label='<strong>I agree to the Code of Conduct (required)</strong>',help_text='By checking, you agree to abide by all <a href="/policies/">Shimmytown Policies</a>, including the <a href="/policies/conduct/">Code of Conduct</a>.')
    mailList = forms.BooleanField(required=False,label='Add me to the Shimmytown mailing list', help_text='Get occasional updates. We make sure that it\'s easy to unsubscribe if you change your mind.')
    # isMinor = forms.BooleanField(required=False,label='I am less than 18 years of age')
    gift = forms.CharField(required=False,label=_('Voucher ID'))
    howHeardAboutUs = forms.ChoiceField(choices=HOW_HEARD_CHOICES,required=False,label='How did you hear about us?',help_text='Optional')

    def get_top_layout(self):

        top_layout = Layout(
            Div('firstName', 'lastName', 'email', css_class='form-inline'),
            Div('phone', css_class='form-inline'),
        )
        return top_layout


    def get_mid_layout(self):
        mid_layout = Layout(
            Div(
                'agreeToPolicies',
                'student',
                'mailList',
                # Div('isMinor',data_toggle="collapse",data_target="#minorAlert"),
                # Alert('Before attending classes, we require all individuals under the age of 18 to have a waiver signed by their guardian. We may also require a guardian to be present. We do not currently offer classes for students under the age of 12.',css_id='minorAlert',css_class="alert-info collapse"),
                css_class='well'),
        )
        return mid_layout

    def get_bottom_layout(self):
        bottom_layout = Layout(
            Div('gift', css_class='form-inline'),
            Div('howHeardAboutUs', css_class='form-inline'),
            'comments',
        )
        return bottom_layout


class QuerysetForm(forms.Form):
    existingQuery = forms.ModelChoiceField(label='Saved Query (add via model admin in management app)',required=False,help_text='Select from an existing query if one has been saved.',queryset=DatabaseQuery.objects.none())
    model = forms.ChoiceField(required=False,choices=get_model_choices(),help_text='Choose from the existing models here.')
    queryset = forms.CharField(required=False,max_length=1000,help_text='Enter the queryset to be executed here.  Only querysets will be processed, not individual objects.')
    fields = forms.CharField(required=False,help_text='Optionally, add one field or property per line to be included in the output.  Use the \'.\' to access foreign key properties, and pass arguments to methods in parentheses.  Also, optionally put headers before an equals sign to define titles for the header row (e.g. for User class, \'Full Name\'=get_full_name). If left blank, all fields will be exported.',widget=forms.Textarea(attrs={'rows': 6, 'cols': 80}))

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user', None)
        super(self.__class__,self).__init__(*args,**kwargs)
        if self.user.is_superuser:
            self.fields['existingQuery'].queryset = DatabaseQuery.objects.all()
        else:
            self.fields['existingQuery'].queryset = DatabaseQuery.objects.filter(requiredGroup__in=self.user.groups.all())
            del self.fields['model']
            del self.fields['queryset']
            del self.fields['fields']

    def clean(self):
        cleaned_data = super(QuerysetForm, self).clean()
        existingQuery = cleaned_data.get('existingQuery')
        model = cleaned_data.get('model')
        queryset = cleaned_data.get('queryset')
        fields = cleaned_data.get('fields')

        if existingQuery and (model or queryset or fields):
            raise ValidationError('Cannot execute both an existing query and a new query; select only one.',code='invalid')
        elif not self.user.is_superuser and (existingQuery.requiredGroup not in self.user.groups.all()):
            raise ValidationError('You do not have permission to execute this query.')
        elif (model and queryset) and (model.split('.')[-1] != queryset.split('.')[0]):
            raise ValidationError('Queryset does not match model.', code='invalid')
