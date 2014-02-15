"""
Django settings for base project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import dirname, join, realpath
from sys import path

ROOT = realpath(join(dirname(__file__), '..'))
BASE_PATH = realpath(join(ROOT, '..'))

path[0:0] = [
    join(ROOT, 'apps'),
    join(ROOT, 'core'),
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h_576od1kr201z-3l878)w+jdgr4dxr7#7p66+t+h%t8$0h*yo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'celery',
    'pipeline',
    'responses.core',
    'crispy_forms',
    'base',
    'projects',
    'south'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
)

ROOT_URLCONF = 'responses.urls'

WSGI_APPLICATION = 'responses.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_ROOT = join(BASE_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = join(BASE_PATH, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

PIPELINE_CSS = {
    'main-css': {
        'source_filenames': (
            'css/main.css',
            'vendors/bootstrap/css/bootstrap.css',
        ),
        'output_filename': 'compress/css/main.min.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    }
}
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

PIPELINE_JS = {
    'main-js': {
        'source_filenames': (
            'js/main.js',
            'vendors/bootstrap/js/bootstrap.js',
        ),
        'output_filename': 'compress/js/main.min.js',
    },
}
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'


STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

# Jinja2
JINGO_INCLUDE_PATTERN = r'\.jinja2'
JINJA_CONFIG = {
    'autoescape': False,
    'extensions': [
        'jinja2.ext.i18n',
        'jinja2.ext.with_',
        'pipeline.jinja2.ext.PipelineExtension'
    ]
}

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# celery
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# projects
MAX_URL_CHECK = 300
