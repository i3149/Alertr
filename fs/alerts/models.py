from django.db import models

class User(models.Model): 
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('D', 'Deleted'),
    )
    user_tag   = models.CharField(max_length=30, db_index=True, unique=True)
    cdate      = models.DateTimeField(auto_now=True)
    status     = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

class Contact(models.Model):
    CONTACT_CHOICES = (
        ('E', 'Email'),
        ('S', 'SMS'),
    )
    ctype  = models.CharField(max_length=1, choices=CONTACT_CHOICES)
    value  = models.CharField(max_length=64)
    user   = models.ForeignKey(User)

class Node(models.Model):
    node_tag = models.CharField(max_length=30, db_index=True, unique=True)
    user     = models.ForeignKey(User)
    high     = models.BigIntegerField()
    low      = models.BigIntegerField()

class Alert(models.Model):
    node   = models.ForeignKey(Node)
    key    = models.CharField(max_length=30, db_index=True, unique=False)
    value  = models.BigIntegerField()
    cdate  = models.DateTimeField(auto_now=True)
    adate  = models.DateTimeField(null=True)
