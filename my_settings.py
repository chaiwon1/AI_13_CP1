# my database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'cp1db',
        'USER' :'chaiwon',
        'PASSWORD' : 'codestatesteam06',
        'HOST' : 'cp1.chlrzs6niw0m.ap-northeast-2.rds.amazonaws.com',
        'PORT' : '3306',
        'OPTIONS' : {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        },
    }
}

SECRET_KEY = 'django-insecure-0_7eu9(*fbzl^2c8(0(x^#1&mte2&=hvjf)u@j!%ox%30)1fc8'