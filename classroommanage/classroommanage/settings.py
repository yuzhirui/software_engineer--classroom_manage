# -*- coding: utf-8 -*-
"""
Django settings for classroommanage project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'imze5e1e!w-_a3z=1y*qcvrdbv6tw^@j7heyh3se7a@-+ws!=x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'classroom',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'classroommanage.urls'

WSGI_APPLICATION = 'classroommanage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'roomdb',
        'USER': 'root',
        'PASSWORD': 'yuzhirui',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
# Additional locations of static files
STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static')
STATICFILES_DIRS = (
    ('css',os.path.join(STATIC_ROOT,'css').replace('\\','/') ),  
    ('js',os.path.join(STATIC_ROOT,'js').replace('\\','/') ),
    ('images',os.path.join(STATIC_ROOT,'images').replace('\\','/')),
)

#邮件配置
EMAIL_HOST = 'smtp.163.com'                   #SMTP地址
EMAIL_PORT = 25                                 #SMTP端口
EMAIL_HOST_USER = '18994855609@163.com'       #我自己的邮箱
EMAIL_HOST_PASSWORD = 'yzr070547'                  #我的邮箱密码
EMAIL_SUBJECT_PREFIX = u'[HIT教室管理网]'            #为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True                             #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
#管理员站点
SERVER_EMAIL = '18994855609@163.com'            #The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
