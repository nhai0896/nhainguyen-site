import datetime

from django.db import models
from django.utils import timezone

class Message(models.Model):
    bank_message = models.CharField(max_length=500)
    """pub_date = models.DateTimeField('date published')
    def _str_(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)"""
    bank = models.CharField(max_length=500)
    tk = models.CharField(max_length=500)
    time = models.CharField(max_length=500)
    amount = models.CharField(max_length=500)
    currency = models.CharField(max_length=500)
    content = models.CharField(max_length=500)
    service = models.CharField(max_length=500)
