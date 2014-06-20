from django.db import models

# Models for the sfb-shop


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    pass