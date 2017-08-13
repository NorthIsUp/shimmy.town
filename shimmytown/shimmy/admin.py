from django.contrib import admin
from django.forms import ModelForm, ChoiceField
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import DatabaseQuery, RecommendedSong, IPNMessage, IPNCartItem
from .helpers import get_model_choices


class DatabaseQueryForm(ModelForm):
    model = ChoiceField(choices=get_model_choices())


class DatabaseQueryAdmin(admin.ModelAdmin):
    list_display = ('name','model','execute_link')
    list_filter = ('model',)
    form = DatabaseQueryForm

    def execute_link(self,obj):
        return '<a href="%s" class="btn btn-default">Execute</a>' % reverse('submitquery')
    execute_link.allow_tags = True


class RecommendedSongAdmin(admin.ModelAdmin):
    list_display = ('title','artist','album','bpm','genre','publish')
    list_display_links = ('title',)
    list_editable = ('artist','album','bpm','genre','publish')

    list_filter = ('genre',)


class IPNCartItemInline(admin.StackedInline):
    model = IPNCartItem
    extra = 0
    exclude = ['revenueItem',]

    def get_readonly_fields(self, request, obj=None):
        always_readonly = ['invoiceName','invoiceNumber','mc_gross','revenueItemLink']

        if request.user.has_perm('paypal.allocate_refunds') or request.user.is_superuser:
            return always_readonly
        else:
            return ['refundAmount'] + always_readonly

    def get_admin_change_link(self,app_label, model_name, obj_id, name):
        url = reverse('admin:%s_%s_change' % (app_label, model_name),
                      args=(obj_id,))
        return format_html('<a href="%s">%s</a>' % (
            url, str(name)
        ))

    def revenueItemLink(self,item):
        if item.initialCartItem.revenueItem:
            ri = item.initialCartItem.revenueItem
            return self.get_admin_change_link('financial','revenueitem',ri.id,ri.__str__())
        else:
            return None
    revenueItemLink.allow_tags = True
    revenueItemLink.short_description = _('Revenue Item')


class IPNMessageAdmin(admin.ModelAdmin):

    def get_admin_change_link(self,app_label, model_name, obj_id, name):
        url = reverse('admin:%s_%s_change' % (app_label, model_name),
                      args=(obj_id,))
        return format_html('<a href="%s">%s</a>' % (
            url, str(name)
        ))

    def finalRegistrationLink(self,item):
        if item.initialTransaction.finalRegistration:
            fr = item.initialTransaction.finalRegistration
            return self.get_admin_change_link('core','registration',fr.id,fr.__str__())
        else:
            return None
    finalRegistrationLink.allow_tags = True
    finalRegistrationLink.short_description = _('Final Registration')

    def registrationLink(self,item):
        if item.initialTransaction.registration:
            tr = item.initialTransaction.registration
            return self.get_admin_change_link('core','temporaryregistration',tr.id,tr.__str__())
        else:
            return None
    registrationLink.allow_tags = True
    registrationLink.short_description = _('Initial Temporary Registration')

    def priorTransactionLink(self,item):
        if item.priorTransaction:
            pt = item.priorTransaction
            return pt.payment_status + ': ' + self.get_admin_change_link('paypal','ipnmessage',pt.id,pt.txn_id) + '<br />'
        else:
            return None
    priorTransactionLink.allow_tags = True
    priorTransactionLink.short_description = _('Prior Transaction')

    def subsequentTransactionLinks(self,item):
        if item.subsequenttransactions.all():
            return '&nbsp;'.join([
                st.payment_status + ': ' + self.get_admin_change_link('paypal','ipnmessage',st.id,st.txn_id) + '<br />'
                for st in item.subsequenttransactions.all()
            ])
    subsequentTransactionLinks.allow_tags = True
    subsequentTransactionLinks.short_description = _('Subsequent Transactions')

    def existingInvoiceLink(self,item):
        if item.paypalInvoice:
            inv = item.paypalInvoice
            return self.get_admin_change_link('paypal','invoice',inv.id,item.generated_invoice)
        else:
            return item.generated_invoice
    existingInvoiceLink.allow_tags = True
    existingInvoiceLink.short_description = _('Paypal-Generated Invoice')

    inlines = [IPNCartItemInline,]

    list_display = ['id','registration','invoice','txn_id','payment_date','mc_gross','mc_fee','payment_status','payer_email']
    list_filter = ['payment_date','payment_status']
    search_fields = ['registration__firstName','registration__lastName','payer_email','txn_id','invoice']
    ordering = ['-payment_date',]
    readonly_fields = ['existingInvoiceLink','unallocatedRefunds','finalRegistrationLink','priorTransactionLink','subsequentTransactionLinks','registrationLink','netRevenue','invoice','payment_date','mc_gross','mc_fee','payment_status','txn_id','payer_id','payer_email','receiver_email','txn_type','mc_currency','custom']
    exclude = ['finalRegistration','registration','priorTransaction','generated_invoice']

    fieldsets = (
        (_('Overall Transaction Information'), {
            'fields': ('invoice','existingInvoiceLink','finalRegistrationLink','registrationLink','netRevenue','unallocatedRefunds'),
        }),
        (_('Related Transactions'), {
            'fields': ('priorTransactionLink','subsequentTransactionLinks',),
        }),
        (_('This IPN Message'), {
            'fields': ('txn_id','payment_date','mc_gross','mc_fee','payment_status','payer_id','payer_email','receiver_email','txn_type','mc_currency','custom'),
        }),
    )


admin.site.register(RecommendedSong, RecommendedSongAdmin)
admin.site.register(DatabaseQuery, DatabaseQueryAdmin)
admin.site.register(IPNMessage, IPNMessageAdmin)
