# -*- coding: utf-8 -*- 
from mezzanine.project_template.settings import *
import os

# Paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)

INSTALLED_APPS = (
    "main", # the main app
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.accounts",

    # =persona for authentication
    "django_browserid",
    
    # south for migrations
    "south",
)

# from /fn-env/src/mezzanine/mezzanine/project_template
AUTHENTICATION_BACKENDS = (
    "mezzanine.core.auth_backends.MezzanineBackend",
    "django_browserid.auth.BrowserIDBackend", # =persona
)

ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = (
    # "username",
    "email",
    "first_name",
    "last_name",
    "password",
    "password_1",
    "password_2",
)

# from /fn-env/src/mezzanine/mezzanine/project_template
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "mezzanine.conf.context_processors.settings",
    "django_browserid.context_processors.browserid", # =persona
)

# LOGIN_REDIRECT_URL = '/' # =persona
LOGIN_REDIRECT_URL_FAILURE = '/' # =persona
LOGOUT_REDIRECT_URL = '/' # =persona

MIDDLEWARE_CLASSES = (["mezzanine.core.middleware.UpdateCacheMiddleware"] +
                      list(MIDDLEWARE_CLASSES) +
                      ["mezzanine.core.middleware.FetchFromCacheMiddleware"])
MIDDLEWARE_CLASSES.remove("mezzanine.pages.middleware.PageMiddleware")

# Mezzanine
AUTH_PROFILE_MODULE = "main.Profile"
SITE_TITLE = "Food News"
RATINGS_RANGE = (-1, 1)
RATINGS_ACCOUNT_REQUIRED = True
COMMENTS_ACCOUNT_REQUIRED = True
ACCOUNTS_PROFILE_VIEWS_ENABLED = True

# Drum
ALLOWED_DUPLICATE_LINK_HOURS = 24 * 7 * 3
ITEMS_PER_PAGE = 30

try:
    from local_settings import *
except ImportError:
    pass

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
