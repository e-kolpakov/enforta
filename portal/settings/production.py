# -*- coding=utf-8 -*-

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

# Адрес сервера (используется для создания ссылок в почтовых сообщениях)
ROOT_URL = "http://87.241.226.36"

# Настройки сервера исходящей почты
EMAIL_HOST = 'enforta.com'
EMAIL_HOST_USER = 'infoservice@enforta.com'
EMAIL_HOST_PASSWORD = 'ctlueess'
EMAIL_PORT = '25'
EMAIL_USE_TLS = 'False'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Почтовые адреса для уведомлений о критических ошибках
ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#Период времени по истечении которого пользователям будут высылаться напоминания о необходимых действиях
# Формат "D day(s) HH:MM:SS
NOTIFICATIONS_TIMEOUT = '2 days 00:00:00'

#Частота отправки напоминаний
# Формат "D day(s) HH:MM:SS
NOTIFICATIONS_FREQUENCY = '1 day 00:00:00'

# Изменения в следующих параметрах могут потребовать реконфигурации сервера.
# См. инструкцию по настройке приложения

#Путь в файловой системе сервера для долговременного хранения загружаемых файлов.
MEDIA_ROOT = "/var/uploads/doc-approval"

# Временная зона сервера. Список временных зон доступен по адресу
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Moscow'

#Максимальный размер загружаемого файла (в Кб) - ниже приведено значение по умолчанию
# MAX_FILE_SIZE = 5120

# Разрешенные к загрузке типы файлов - ниже приведены значения по умолчанию
# ALLOWED_MIME_TYPES = (
#     'application/pdf',
#     'application/x-pdf',
#     'image/tiff',
#     'image/x-tiff',
#     'image/jpeg',
#     'image/pjpeg',
#     'application/msword',
#     'application/excel',
#     'application/vnd.ms-excel',
#     'application/x-excel',
#     'application/x-msexcel',
#     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
# )
