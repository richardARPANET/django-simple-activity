import os
from os.path import abspath, dirname
from importd import d

DJANGO_ROOT = dirname(dirname(abspath(__file__)))
DEBUG = False


def pytest_configure():
    d(
        DJANGO_ROOT=dirname(dirname(abspath(__file__))),
        DEBUG=False,
        TEMPLATE_DEBUG=DEBUG,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'testactivitydb',
                'USER': 'testactivity',
                'PASSWORD': 'testactivity',
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
