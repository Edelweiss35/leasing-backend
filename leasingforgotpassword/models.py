# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from leasingauth.models import LeasingUser
                                
class LeasingResetPassword(models.Model):
    client = models.ForeignKey(LeasingUser, related_name="client",
                               on_delete=models.CASCADE)
    hash = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
                                
    def __str__(self):
        return '%s %s' % (self.client.id, self.active)
