from __future__ import absolute_import

from .env import log_setting


def patch_pipeline(g):
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.9/howto/static-files/
    g['BOOTSTRAP_VERSION'] = 4

    g['INSTALLED_APPS'] += ['pipeline']

    # if g['DEBUG']:
    #     g['STATICFILES_STORAGE'] = 'pipeline.storage.PipelineCachedStorage'

    g['STATICFILES_FINDERS'] = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'pipeline.finders.PipelineFinder',
    )

    g['PIPELINE'] = {
        'SHOW_ERRORS_INLINE': False,

        # 'PIPELINE_ENABLED': False,
        # 'PIPELINE_COLLECTOR_ENABLED': True,
        'STYLESHEETS': {
            'app': {
                'source_filenames': (
                    'scss/app.scss',
                    # 'css/*.css',
                ),
                'output_filename': 'css/app.css',
            },
        },
        'COMPILERS': (
            'pipeline.compilers.sass.SASSCompiler',
        ),
        'CSS_COMPRESSOR': None,
        # 'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
        # 'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
        # 'YUGLIFY_BINARY': BASE_DIR / 'node_modules' / '.bin' / 'yuglify',
        'SASS_BINARY': '/usr/bin/env python -m sassc',
        'SASS_ARGUMENTS': ' '.join(
            ['--source-comments'] + ['-I {}'.format(d) for d in  (
                g['STATIC_ROOT'] / 'bootstrap{BOOTSTRAP_VERSION}/scss'.format(**g),
                # g['BASE_DIR'] / 'bower_components/motion-ui/src',
            )]
        ),
    }

    g['STATIC_ROOT'] = g['BASE_DIR'] / 'static'
    g['CRISPY_TEMPLATE_PACK'] = 'bootstrap{BOOTSTRAP_VERSION}'.format(**g)
