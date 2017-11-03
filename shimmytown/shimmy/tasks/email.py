# -*- coding: utf-8 -*-

from __future__ import absolute_import

# Standard Library
from logging import getLogger

# External Libraries
from django.conf import settings
from huey.contrib.djhuey import db_task
from mailsnake import MailSnake

logger = getLogger(__name__)


@db_task(retries=3)
def add_customer_to_mailing_list(customer):
    '''
    When called, this adds the customer's email to the mailing list.
    '''
    if not hasattr(settings,'MAILCHIMP_API_KEY') or not hasattr(settings,'MAILCHIMP_LIST_ID'):
        logger.info('Did not update mailing list to add customer %s, MailChimp is not set up.' % customer.id)
        return

    logger.info('Updating mailing list in MailChimp, adding customer %s.' % customer.id)
    ms = MailSnake(settings.MAILCHIMP_API_KEY)
    listId = settings.MAILCHIMP_LIST_ID

    ms.listSubscribe(
        id=listId,
        email_address=customer.email,
        email_type='html',
        double_optin=False,
        update_existing=True,
        merge_vars={
            'FNAME': customer.first_name,
            'LNAME': customer.last_name
        })
