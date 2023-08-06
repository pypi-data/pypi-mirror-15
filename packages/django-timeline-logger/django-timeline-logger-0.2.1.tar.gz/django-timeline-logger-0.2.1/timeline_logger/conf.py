from __future__ import unicode_literals

from django.conf import settings

from appconf import AppConf


class TimelineLoggerConf(AppConf):

    DEFAULT_TEMPLATE = 'timeline_logger/default.txt'

    PAGINATE_BY = 25

    class Meta:
        prefix = 'timeline'
