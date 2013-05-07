# -*- coding=utf-8 -*-
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docapproval',
        'USER': 'docapprovaluser',
        'PASSWORD': 'dau!w3aker_p@ssword',
        'HOST': 'localhost',
        'PORT': '',
    }
}

#Конфигурационные параметры

# FQDN или IP-адрес сервера
ALLOWED_HOSTS = '*'

# Почтовые адреса для уведомлений о критических ошибках
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

#Максимальный размер загружаемого файла (в Кб)
MAX_FILE_SIZE = 5120

#Период времени по истечении которого пользователям будут высылаться напоминания о необходимых действиях
NOTIFICATIONS_TIMEOUT = '2 days'

#Частота отправки напоминаний
NOTIFICATIONS_FREQUENCY = '1 day'

#Основной e-mail адрес для оповощения бухгалтерии
ACCOUNTING_EMAIL = 'accounting@enforta.ru'

# Изменения в следующих параметрах могут потребовать реконфигурации сервера.
# См. инструкцию по настройке приложения

#Путь в файловой системе сервера для долговременного хранения загружаемых файлов.
MEDIA_ROOT = "/var/uploads/doc-approval"

# Временная зона сервера. Список временных зон доступен по адресу
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Moscow'
