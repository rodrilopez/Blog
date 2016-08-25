# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.mail import send_mail

#notify = False

class Post(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    CATEGORIAS = (
        ("0", 'Trabajos Practicos'),
        ("1", 'Ejemplo'),        
        ("2", 'Otros'),
    )
    categorias = models.CharField(max_length=6,
                                      choices=CATEGORIAS,
                                      default="0")
    url_post = models.CharField(max_length=60, null=True, blank=True)
    
    def __unicode__(self):
        return self.title




### Admin

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    display_fields = ["title", "created","categorias",]
    
# IMPLEMENTADO    
class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=60)
    body = models.TextField()

    def __unicode__(self):
        return self.body

