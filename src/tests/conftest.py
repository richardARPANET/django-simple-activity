import os
import hashlib
import string
import random
from os.path import abspath, basename, dirname

from django.core.exceptions import ImproperlyConfigured
from importd import d
ugettext = lambda s: s


def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)


def get_env_bool(var_name, default=False):
    """Get a boolean environment variable, default to False"""
    try:
        result = os.environ[var_name]
    except KeyError:
        return default
    else:
        if result.lower() in ['0', 'false', 'off']:
            return False
        return True


def get_test_db_name():
    md5 = hashlib.md5()
    to_hash = os.environ.get('BUILD_TAG', b'no-tag')
    md5.update(to_hash)
    return md5.hexdigest()


def gen_string(max_length):
    return u''.join(random.choice(string.ascii_letters)
                    for i in range(max_length))

gen_string.required = ['max_length']

VIDISPINE_USERNAME = 'admin'
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = DJANGO_ROOT
SITE_NAME = basename(DJANGO_ROOT)
log_folder = '/var/log/zonza/'
DEBUG = False
ADMINS = [
    ['Admin', 'admin@zonza.tv'],
]
VIDISPINE_URL = 'http://vidi1-dev-zonza'
VIDISPINE_PORT = '8080'
AUTH_PROFILE_MODULE = 'users.UserProfile'


def pytest_configure():
    d(
        DJANGO_ROOT=dirname(dirname(abspath(__file__))),
        DEBUG=False,
        TEMPLATE_DEBUG=DEBUG,
        MANAGERS=ADMINS,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'jenzonzadb',
                'USER': 'jenzonza',
                'PASSWORD': 'jenzonza',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        },
        ALLOWED_HOSTS=[],
        CSRF_COOKIE_DOMAIN=None,
        TI_TEST=False,
        STATICFILES_FINDERS=[
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        ],
        MESSAGE_STORAGE=[
            'django.contrib.messages.'
            'storage.session.SessionStorage'
        ],
        AUTHENTICATION_BACKENDS=[
            'django.contrib.auth.backends.ModelBackend',
        ],
        ANONYMOUS_USER_ID=-1,
        TEMPLATE_CONTEXT_PROCESSORS=[
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.request",
        ],
        TEMPLATE_LOADERS=[
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        TEMPLATE_DIRS=[
            os.path.join(
                os.path.dirname(
                    __file__), '..', 'templates'
            ).replace('\\', '/'),
        ],
        MIDDLEWARE_CLASSES=[
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            # Uncomment the next line for simple clickjacking protection:
            # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        ROOT_URLCONF='activity.urls',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'activity',
            'django_nose',
        ],
        TEST_RUNNER='django_nose.NoseTestSuiteRunner',
    )
