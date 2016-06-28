# Django settings for my project.
import os

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(APP_ROOT, '..'))

DEVELOPMENT = False
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Kelly Miller', 'kellym@millcreeksoftware.biz'),
)

MANAGERS = ADMINS

DATABASES = {
	'local': {
		'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': '',  # Or path to database file if using sqlite3.
		'USER': '',  # Not used with sqlite3.
		'PASSWORD': '',  # Not used with sqlite3.
		'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',  # Set to empty string for default. Not used with sqlite3.
	},
	'development': {
		'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': os.path.join(PROJECT_ROOT, "sqlite/local.db"),  # Or path to database file if using sqlite3.
		'USER': '',  # Not used with sqlite3.
		'PASSWORD': '',  # Not used with sqlite3.
		'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',  # Set to empty string for default. Not used with sqlite3.
	},
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'lhbweb',  # Or path to database file if using sqlite3.
		'USER': 'lhbweb',  # Not used with sqlite3.
		'PASSWORD': 'Order1webfaction',  # Not used with sqlite3.
		'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',  # Set to empty string for default. Not used with sqlite3.
	}
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'customer_media')
MEDIA_UPLOAD_PATH = os.path.join(MEDIA_ROOT, '/customer_media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/customer_media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 't8%+b87azv!0)#)bc^x!1h*m(ar#z7flxls!r6mu*+pj6n_q!4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.cache.UpdateCacheMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.cache.FetchFromCacheMiddleware',
	'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'webapp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'webapp.wsgi.application'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_ROOT, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.request',
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.static',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.redirects',
	'django.contrib.sitemaps',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# 3rd Party Applications
	'filebrowser',
	'suit',
	'django.contrib.admin',
	'mptt',
	'reversion',
	# My Applications
	'city_metrics',
	'site_content',
	'webapp',
	'webapp_admin',
)

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	},
	'production': {
		'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
		'LOCATION': '/var/tmp/webapp_cache',
		'TIMEOUT': 60,  # 60 seconds
	}
}

SUIT_CONFIG = {
	# header
	'ADMIN_NAME': 'Regional Indicators Initiative',
	'HEADER_DATE_FORMAT': 'l, F jS, Y',
	'HEADER_TIME_FORMAT': 'h:i a',

	# forms
	'SHOW_REQUIRED_ASTERISK': True,  # Default True
	'CONFIRM_UNSAVED_CHANGES': False,  # Default True

	# menu
	'SEARCH_URL': '/admin/auth/user/',
	'MENU_ICONS': {
		'sites': 'icon-leaf',
		'auth': 'icon-lock',
	},
	'MENU_OPEN_FIRST_CHILD': True,  # Default True
	'MENU': (
		{'app': 'auth'},
		{'app': 'city_metrics', 'label': 'City Metrics', 'icon': 'icon-signal'},
		{'app': 'site_content', 'label': 'Site Content', 'icon': 'icon-file'},
		{'label': 'Site Media', 'icon': 'icon-folder-open', 'url': '/admin/filebrowser/browse/'},
		{'label': 'Demo Data Importer', 'icon': 'icon-arrow-up', 'url': '/admin/imports/demographic-data-importer/'},
		{'label': 'Energy Importer', 'icon': 'icon-arrow-up', 'url': '/admin/imports/energy-importer/'},
		{'label': 'Water Importer', 'icon': 'icon-arrow-up', 'url': '/admin/imports/water-importer/'},
		{'label': 'Travel Importer', 'icon': 'icon-arrow-up', 'url': '/admin/imports/travel-importer/'},
		{'label': 'Waste Importer', 'icon': 'icon-arrow-up', 'url': '/admin/imports/waste-importer/'},
		{'label': 'Emissions Importer', 'icon': 'icon-arrow-up', 'url': '/admin/imports/emissions-importer/'},
		{'label': 'Cost Importer', 'icon': 'icon-arrow-up', 'url': '/admin/imports/cost-importer/'},
	),

	# misc
	'LIST_PER_PAGE': 30
}

FILEBROWSER_SUIT_TEMPLATE = True

ANALYTICS_EMAIL = ''
ANALYTICS_PASSWORD = ''
ANALYTICS_TABLE_ID = 'ga:62814676'  # ALWAYS INCLUDE ga: