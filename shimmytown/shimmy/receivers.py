# -*- coding: utf-8 -*-

from __future__ import absolute_import

# Standard Library
from logging import getLogger

# External Libraries
from danceschool.core.signals import post_registration
from django.dispatch import receiver
from shimmy.tasks.email import add_customer_to_mailing_list

logger = getLogger(__name__)

@receiver(post_registration)
def check_for_mailing_list(sender, **kwargs):
    registration = kwargs.get('registration',None)

    if (
        hasattr(registration,'data') and
        isinstance(registration.data,dict) and
        registration.data.get('mailList',None)
    ):
        logger.info('Adding customer to mailing list as requested.')
        add_customer_to_mailing_list(registration.customer)
