# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import EmailLog, EmailQueue
# Register your models here.

admin.site.register(EmailQueue)
admin.site.register(EmailLog)
