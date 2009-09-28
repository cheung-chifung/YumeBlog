# Django settings for yumeblog project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

"""
DATABASE
"""
DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'yumeblog_django'  # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = '127.0.0.1'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'             # Set to empty string for default. Not used with sqlite3.

"""
INSTANCE PATH
"""
#The instance name of your blog
INSTANCE = 'myblog'
#Absolute path to your instance
#INSTANCE_ROOT = '/path/to/your/instance/root'
INSTANCE_ROOT = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))),INSTANCE)
INSTANCE_URL = '/'.join(['http://localhost',INSTANCE])

SITE_ID = 1 #Not to modify if you just want to deploy one instance

"""
TEMPLATE PATH
"""
BLOG_TEMPLATE_DIR = '/LIBPATH/libs/yumeblog/templates' #Path to your folder where template located.Should be an absolute path
TEMPLATE_NAME = 'default' # Your template's name

"""
EDITOR PATH
"""
FCKEDITOR_MEDIA_ROOT = '/LIBPATH/libs/utils/fckeditor/fckeditor' #Set to use a fckeditor
FCKEDITOR_MEDIA_URL = '/'.join([INSTANCE_URL,'fckeditor']) #No need to modify

"""
DFEAULT URLS CONF
"""
ROOT_URLCONF = '%s.urls' % INSTANCE

"""
MODERATION SETTINGS
"""
#AKISMET_API_KEY = 'YOUR_AKISMET_API_KEY'
DELETE_SPAM_COMMENT = False
#BAN_NON_CJK = True

"""
SENDMAIL SETTINGS
"""
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='username@gmail.com'
EMAIL_HOST_PASSWORD='password'
EMAIL_USE_TLS = True

"""
CUSTOM SETTINGS
"""
ITEM_COUNT_PER_PAGE = 10 #The count of entries of per page


"""
DJANGO SETTINGS
"""
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(INSTANCE_ROOT,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://www.hicrokee.com/blog/static'

STATIC_ROOT = os.path.join(INSTANCE_ROOT,'static') #static files folder (for Upload)
STATIC_URL = '/'.join([INSTANCE_ROOT,'static'])      #static files

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/'.join([INSTANCE_ROOT,'media','']) #ADMIN folders

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'l=^7@%4=(+kop)yb-6h+9g_j4abqj#r-b8vm=t#v(7e=64)^hj'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BLOG_TEMPLATE_DIR,TEMPLATE_NAME),
)

TEMPLATE_BLOG_ROOT = os.path.join(BLOG_TEMPLATE_DIR,TEMPLATE_NAME)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'tagging',
    'yumeblog',
)
