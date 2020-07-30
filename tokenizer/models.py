from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Tokenoutput(models.Model):
    textoutput = models.TextField

    def __str__(self):
        return self.textoutput


class Keywords(models.Model):

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    key = models.CharField(max_length=100)
    key_index = models.IntegerField()
    text = models.TextField()
    words = models.TextField()
    words_selected = models.TextField()
    keywords = models.TextField(null=True)

    def __str__(self):
        return self.text



class v1_Keywords(models.Model):

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    session_id = models.CharField(max_length=100)
    session_index = models.IntegerField()
    text = models.TextField()
    words = models.TextField()
    words_selected = models.TextField()
    keywords = models.TextField(null=True)

    def __str__(self):
        return self.text





class keyword_select(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    user_id = models.CharField(max_length=100)
    user_key = models.IntegerField()
    author_id = models.CharField(max_length=100)
    pos_text = models.TextField(null=True)
    neg_text = models.TextField(null=True)
    pos_text_norm = models.TextField(null=True)
    neg_text_norm = models.TextField(null=True)
    pos_keyword = models.TextField(null=True)
    neg_keyword = models.TextField(null=True)
    pos_word_num = models.TextField(null=True)
    neg_word_num = models.TextField(null=True)
    rand_order = models.IntegerField(null=True)

    def __str__(self):
        return self.pos_text



