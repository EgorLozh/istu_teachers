from django.db import models

class Teacher(models.Model):
    site_id = models.IntegerField(blank=True)
    name = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    description = models.TextField(max_length=1000)
    pict = models.CharField(max_length=255)
