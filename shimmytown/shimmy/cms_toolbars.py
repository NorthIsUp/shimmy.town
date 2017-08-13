from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


@toolbar_pool.register
class DatabaseQueryToolbar(CMSToolbar):
    ''' Adds links for BLH-specific content to the content toolbar '''

    def populate(self):
        if self.request.user.has_perm('shimmy.change_recommendedsong'):
            menu = self.toolbar.get_or_create_menu('core-content',_('Content'))
            menu.add_link_item(_('Manage Recommended Music'),reverse('admin:shimmy_recommendedsong_changelist'))
        if self.request.user.has_perm('shimmy.run_database_query'):
            menu = self.toolbar.get_or_create_menu('core-content',_('Content'))
            menu.add_link_item(_('Query the Database'),reverse('submitquery'))

            events_menu = self.toolbar.get_or_create_menu('core-events')
            events_menu.add_link_item(_('MNP Entry List'), reverse('MNPEntryList'))

        if self.request.user.has_perm('shimmy.change_databasequery'):
            menu = self.toolbar.get_or_create_menu('core-content',_('Content'))
            menu.add_link_item(_('Manage Database Queries'),reverse('admin:shimmy_databasequery_changelist'))
