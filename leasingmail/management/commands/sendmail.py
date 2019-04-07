from django.core.management.base import BaseCommand
from leasingmail.models import EmailQueue

class Command(BaseCommand):
  
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        
    def handle(self, *args, **kwargs):
        for queued_mail in EmailQueue.objects.all():
            try:
                queued_mail.send_now = True
                queued_mail.save()
            except Exception as e:
                print("Exception raise while sending the mail %s" % e)
                pass
