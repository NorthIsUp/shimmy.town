from __future__ import absolute_import


def patch_pipeline(g):
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.9/howto/static-files/

    g['STATICFILES_STORAGE'] = 'pipeline.storage.PipelineCachedStorage'
    g['STATICFILES_FINDERS'] = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'pipeline.finders.PipelineFinder',
    )

    g['SHOW_ERRORS_INLINE'] = False
    g['PIPELINE'] = {
        'SHOW_ERRORS_INLINE': False,
        'STYLESHEETS': {
            'app': {
                'source_filenames': (
                    'fonts/*',
                    'scss/*.scss',
                    'css/*.css',
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
        'SASS_ARGUMENTS': ' '.join('-I {}'.format(d) for d in (
            # g['BASE_DIR'] / 'bower_components/foundation-sites/scss',
            # g['BASE_DIR'] / 'bower_components/motion-ui/src',
        )),
    }

    g['STATIC_ROOT'] = g['BASE_DIR'] / 'static'
