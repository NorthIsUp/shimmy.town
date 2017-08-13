from django.db import models
from django.db.models import Q
from django.contrib.auth.models import Group
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from danceschool.core.models import TemporaryRegistration, Registration, Invoice
from danceschool.financial.models import RevenueItem


@python_2_unicode_compatible
class DatabaseQuery(models.Model):
    name = models.CharField(max_length=200,unique=True,help_text='This is what will be shown in the dropdown menu, so make sure this is clear.')
    model = models.CharField(max_length=200,help_text='Select the model to be queried.')
    query = models.CharField(max_length=1000,help_text='This will be evaluated directly and must return a QuerySet, not an individual object.  You have access to your model, its properties, the Q() object, and to datetime.  You do not have access most other builtin methods.')
    fields = models.TextField(null=True,blank=True,help_text='Optionally, add one field or property per line to be included in the output.  Use the \'.\' to access foreign key properties, and pass arguments to methods in parentheses.  Also, optionally put headers before an equals sign to define titles for the header row (e.g. for User class, \'Full Name\'=get_full_name). If left blank, all fields will be exported.')

    requiredGroup = models.ForeignKey(Group,verbose_name='Group Permission Required',null=True,blank=True,help_text='Non superusers can only execute these pre-existing queries if they are in this stated group.  If missing, then only superusers will be able to access this query. Be mindful about giving access.')

    def clean(self):
        if self.model.split('.')[-1] != self.query.split('.')[0]:
            raise ValidationError('Query does not match model.', code='invalid')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Database query'
        verbose_name_plural = 'Database queries'
        ordering = ('name',)
        permissions = (
            ('run_database_query','Access database query page to download pre-specified queries from the database.'),
        )


@python_2_unicode_compatible
class RecommendedSong(models.Model):
    '''
    These record information that was originally in a Google doc.
    '''

    SONG_GENRES = [('Swing','Swing'),('Blues','Blues')]

    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50,null=True,blank=True)
    bpm = models.CharField(max_length=20,null=True,blank=True,help_text='Entering the BPM of the song (if you know it or can calculate it) is very helpful to students.')
    album = models.CharField(max_length=50,null=True,blank=True)
    itunesLink = models.CharField(max_length=100,null=True,blank=True,help_text='Optional: Give students a link to buy the song on iTunes.')
    amazonLink = models.CharField(max_length=100,null=True,blank=True,help_text='Optional: Give students a link to buy the song on Amazon.')
    genre = models.CharField(max_length=20,null=True,blank=True, choices=SONG_GENRES)
    comments = models.TextField(null=True,blank=True,help_text='Comments are for internal use only and are not displayed on the page.')
    publish = models.BooleanField(default=True,help_text='Leave this box unchecked if you want someone to review your contribution before it is published.')
    recommender = models.CharField(max_length=30,null=True,blank=True,help_text='Leave your name here (for internal use only.')

    def __str__(self):
        return self.artist + ' ' + self.title

    class Meta:
        ordering = ('title','artist')


@python_2_unicode_compatible
class IPNMessage(models.Model):
    '''
    Paypal sends IPN messages when a payment is made.
    '''
    message = models.TextField(null=True,blank=True)

    invoiceObject = models.ForeignKey(Invoice,verbose_name=_('Registration Invoice'),null=True)

    registration = models.ForeignKey(TemporaryRegistration,verbose_name=_('Initial Temporary Registration'), null=True)
    finalRegistration = models.OneToOneField(Registration,verbose_name=_('Final Registration'),null=True)
    priorTransaction = models.ForeignKey('self',related_name='subsequenttransactions',null=True)

    invoice = models.CharField(max_length=80,verbose_name=_('Invoice number'))
    generated_invoice = models.CharField(max_length=100,verbose_name=_('Paypal-generated invoice number'),null=True,blank=True)
    mc_fee = models.FloatField()
    mc_gross = models.FloatField()
    payment_status = models.CharField(max_length=30)
    payment_date = models.DateTimeField()
    txn_id = models.CharField(max_length=30,unique=True)
    txn_type = models.CharField(max_length=30)
    custom = models.TextField()
    mc_currency = models.CharField(max_length=30)
    payer_email = models.EmailField()
    receiver_email = models.EmailField()
    payer_id = models.CharField(max_length=30)

    @property
    def netRevenue(self):
        if self.priorTransaction:
            return self.priorTransaction.netRevenue
        else:
            refunds = sum([x.mc_gross - x.mc_fee for x in self.subsequenttransactions.all()])
            return self.mc_gross - self.mc_fee + refunds

    @property
    def totalFees(self):
        if self.priorTransaction:
            return self.priorTransaction.totalFees
        else:
            return sum([x.mc_fee for x in self.subsequenttransactions.all()])

    @property
    def initialTransaction(self):
        if self.priorTransaction:
            return self.priorTransaction
        else:
            return self

    @property
    def relatedTransactions(self):
        return IPNMessage.objects.filter(Q(txn_id=self.txn_id) | Q(priorTransaction=self) | Q(subsequenttransactions=self))

    @property
    def totalReceived(self):
        return sum([x.mc_gross - x.mc_fee for x in self.relatedTransactions.filter(payment_status='Completed')])

    @property
    def totalRefunded(self):
        return -1 * sum([x.mc_gross for x in self.relatedTransactions.filter(payment_status='Refunded')])

    @property
    def unallocatedRefunds(self):
        return self.totalRefunded - sum([x.totalRefunds for x in self.ipncartitem_set.all()])

    def __str__(self):
        return self.invoice + " " + self.payer_email + " " + self.registration.__str__()

    def clean(self):
        # Non-initial transactions cannot also have subsequent transactions.
        if self.priorTransaction and self.subsequenttransactions.all():
            raise ValidationError(_('IPN cannot have both a prior transaction and subsequent transactions.'))

    class Meta:
        verbose_name = _('Paypal IPN message')


class IPNCartItem(models.Model):
    ipn = models.ForeignKey(IPNMessage)
    revenueItem = models.ForeignKey(RevenueItem,null=True,blank=True)

    invoiceName = models.CharField(_('Invoice Item Name'), max_length=100,null=True,blank=True)
    invoiceNumber = models.CharField(_('Invoice Item Number'),max_length=50)
    mc_gross = models.FloatField(_('Gross Amount'),default=0)

    refundAmount = models.FloatField(_('Allocated Refund Amount'),default=0)

    @property
    def initialCartItem(self):
        if self.ipn.priorTransaction:
            return self.ipn.initialTransaction.ipncartitem_set.get(invoiceNumber=self.invoiceNumber)
        else:
            return self

    @property
    def relatedCartItems(self):
        return IPNCartItem.objects.filter(invoiceNumber=self.invoiceNumber).filter(Q(ipn__txn_id=self.ipn.txn_id) | Q(ipn__priorTransaction=self.ipn) | Q(ipn__subsequenttransactions=self.ipn)).distinct()

    # The following properties assume that all invoice items take the format
    # 'TYPE_TYPEID_ITEMID', which is enforced in the Core app and should be
    # enforced elsewhere so that we can parse the invoiceNumbers.
    @property
    def invoiceItemTypeName(self):
        return self.invoiceNumber.split('_')[0]

    @property
    def invoiceItemTypeId(self):
        try:
            return int(self.invoiceNumber.split('_')[1])
        except ValueError:
            return self.invoiceNumber.split('_')[1]

    @property
    def invoiceItemId(self):
        try:
            return int(self.invoiceNumber.split('_')[2])
        except ValueError:
            return self.invoiceNumber.split('_')[2]

    # The following property allocates the discounted total of an IPN Payment
    # across the items in the cart.  This is how revenue received is set
    # after successful IPN payments are used to create EventRegistrations.
    @property
    def allocatedNetPrice(self):
        return \
            self.mc_gross * (self.ipn.mc_gross / sum([
                x.mc_gross for x in self.ipn.ipncartitem_set.all()
            ]))

    @property
    def allocatedFees(self):
        return \
            self.ipn.mc_fee * (self.mc_gross / sum([
                x.mc_gross for x in self.ipn.ipncartitem_set.all()
            ]))

    @property
    def allocatedNetTotal(self):
        return sum([x.allocatedNetPrice for x in self.relatedCartItems.filter(ipn__payment_status='Completed')])

    @property
    def allocatedAdjustment(self):
        return sum([x.allocatedNetPrice for x in self.relatedCartItems.filter(ipn__payment_status='Refunded')])

    @property
    def allocatedTotalFees(self):
        return sum([x.allocatedFees for x in self.relatedCartItems.all()])

    @property
    def totalRefunds(self):
        return sum([x.refundAmount for x in self.relatedCartItems.filter(ipn__payment_status='Refunded')])

    def clean(self):
        # Non-initial transactions cannot also have subsequent transactions.
        if self.refundAmount != 0 and self.ipn.payment_status != 'Refunded':
            raise ValidationError(_('Refunds cannot be allocated for non-refund transaction types.'))

    class Meta:
        verbose_name = _('Paypal IPN Cart Item')
