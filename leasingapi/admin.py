# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from leasingapi.models import (ClientSetting, DocumentUpload, LegalPosition, ExportResult, KeyText, Description)

# Register your models here.
admin.site.register(ClientSetting)
admin.site.register(DocumentUpload)
admin.site.register(LegalPosition)
admin.site.register(ExportResult)
admin.site.register(KeyText)
admin.site.register(Description)
