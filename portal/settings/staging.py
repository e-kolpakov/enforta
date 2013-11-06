# -*- coding=utf-8 -*-

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docapproval_staging',
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

# Адрес сервера (используется для создания ссылок в почтовых сообщениях)
ROOT_URL = "http://87.241.226.36:8080"

# Настройки сервера исходящей почты
EMAIL_HOST = 'enforta.com'
EMAIL_HOST_USER = 'infoservice@enforta.com'
EMAIL_HOST_PASSWORD = 'ctlueess'
EMAIL_PORT = '25'
EMAIL_USE_TLS = 'False'
EMAIL_REDIRECT = ''
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#Период времени по истечении которого пользователям будут высылаться напоминания о необходимых действиях
NOTIFICATIONS_TIMEOUT = '2 days'

#Частота отправки напоминаний
NOTIFICATIONS_FREQUENCY = '1 day'

# Изменения в следующих параметрах могут потребовать реконфигурации сервера.
# См. инструкцию по настройке приложения

#Путь в файловой системе сервера для долговременного хранения загружаемых файлов.
MEDIA_ROOT = "/var/uploads/doc-approval-staging"

# Временная зона сервера. Список временных зон доступен по адресу
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Moscow'

#Максимальный размер загружаемого файла (в Кб)
# MAX_FILE_SIZE = 5120

# Разрешенные к загрузке типы файлов
# ALLOWED_MIME_TYPES = (
#     'application/pdf',
#     'application/x-pdf',
#     'Image/tiff',
#     'image/x-tiff',
#     'Image/jpeg',
#     'image/pjpeg',
#     'application/msword',
#     'application/excel',
#     'application/vnd.ms-excel',
#     'application/x-excel',
#     'application/x-msexcel',
#     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
# )
