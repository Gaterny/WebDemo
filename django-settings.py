#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 配置mysql数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'root',
        'PASSWORD': 'xxxxxx',
        'HOST': '',  # 默认localhost
        'PORT': '',  # 默认8000
    }
}

# 如下设置放置的与project同名的配置的 __init__.py文件中
import pymysql

pymysql.install_as_MySQLdb()

# 配置语言与时区
LANGUAGE_CODE = 'zh-Hans'#语言

TIME_ZONE = 'Asia/Shanghai' #时区

# 配置静态文件路径
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static')
)

# 配置模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 配置上传文件夹
MEDIA_URL = '/media/'  # 设置媒体文件的相对路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 设置媒体文件的绝对路径

STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static'),
   os.path.join(BASE_DIR, 'media'),
)