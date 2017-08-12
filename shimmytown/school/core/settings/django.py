# -*- coding: utf-8 -*-

from __future__ import absolute_import

# External Libraries
from school.core.settings import log_setting
from school.core.settings.env import (
    DEBUG,
    LOCAL,
)


def patch_django(g):
    if LOCAL:
        g['INSTALLED_APPS'] += [
        ]

        g['MIDDLEWARE'] += [
        ]

    if DEBUG:
        log_setting('DEBUG_TOOLBAR', 'is on')

        g['DEBUG'] = DEBUG
        g['PAYPAL_TEST'] = DEBUG
        g['INTERNAL_IPS'] = ['127.0.0.1', ]
        g['DEBUG_TOOLBAR_PATCH_SETTINGS'] = False
        g['INSTALLED_APPS'] += [
            # 'debug_panel',
            'debug_toolbar',
            'django_extensions',
            # 'devserver',
        ]

        g['MIDDLEWARE'] = [
        ] + g['MIDDLEWARE'] + [
            'debug_toolbar.middleware.DebugToolbarMiddleware',

            # For AJAX requests https://github.com/recamshak/django-debug-panel
            # 'debug_panel.middleware.DebugPanelMiddleware',

            # 'tempest.core.middleware.ProcessExceptionMiddleware',
            # 'devserver.middleware.DevServerMiddleware',
        ]

        g['DEBUG_TOOLBAR_PANELS'] = [
            'debug_toolbar.panels.versions.VersionsPanel',
            'debug_toolbar.panels.timer.TimerPanel',
            'debug_toolbar.panels.settings.SettingsPanel',
            'debug_toolbar.panels.headers.HeadersPanel',
            'debug_toolbar.panels.request.RequestPanel',
            'debug_toolbar.panels.sql.SQLPanel',
            'debug_toolbar.panels.staticfiles.StaticFilesPanel',
            'debug_toolbar.panels.templates.TemplatesPanel',
            'debug_toolbar.panels.cache.CachePanel',
            # 'debug_toolbar.panels.signals.SignalsPanel',
            'debug_toolbar.panels.logging.LoggingPanel',
            'debug_toolbar.panels.redirects.RedirectsPanel',
            # 'debug_toolbar.panels.profiling.ProfilingPanel',
            # 'debug_toolbar_line_profiler.panel.ProfilingPanel',
        ]

        g['DEVSERVER_MODULES'] = (
            'devserver.modules.sql.SQLRealTimeModule',
            'devserver.modules.sql.SQLSummaryModule',
            'devserver.modules.profile.ProfileSummaryModule',

            # Modules not enabled by default
            'devserver.modules.ajax.AjaxDumpModule',
            'devserver.modules.profile.MemoryUseModule',
            'devserver.modules.cache.CacheSummaryModule',
            'devserver.modules.profile.LineProfilerModule',
        )
