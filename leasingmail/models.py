# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from leasingforgotpassword.models import LeasingResetPassword
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
# Create your models here.


class EmailLog(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    to_email = models.CharField(max_length=255)
    from_email = models.CharField(max_length=255)
    send_now = models.BooleanField(default=False)
    reset_password = models.ForeignKey(LeasingResetPassword, related_name='user_reset_password', on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s - %s" % (self.to_email, self.subject)


class EmailQueue(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    to_email = models.CharField(max_length=255)
    from_email = models.CharField(max_length=255)
    send_now = models.BooleanField(default=False)
    reset_password = models.OneToOneField(LeasingResetPassword, related_name='reset_password', on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s - %s" % (self.to_email, self.subject)

@receiver(post_save, sender=EmailQueue, dispatch_uid="send_now_then_delete")
def send_now_the_delete(sender, instance, *args, **kwargs):
    """                                                                                                                                                                                                                                                                    
    send emails instantly if send_now=True and then delete the instance                                                                                                                                                                                                    
    """
    
    
    if(instance.send_now):
        email_message = EmailMessage(instance.subject,
                                     instance.body,
                                     settings.POSTMARK_SENDER,
                                     [instance.to_email, ],
                                     bcc=settings.BCC_EMAILS)
        email_message.content_subtype = 'html'
        mail_sent = email_message.send(fail_silently=True)
        
        if(mail_sent == 1):
            email_log = EmailLog.objects.create(from_email=instance.from_email,
                                                subject = instance.subject,
                                                body = instance.body,
                                                to_email = instance.to_email,
                                                reset_password = instance.reset_password)
            instance.delete()
        else:
            print("mail was not sent, mail_sent=%s" % mail_sent)
