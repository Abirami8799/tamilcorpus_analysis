# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Demo(models.Model):
    id = models.IntegerField(primary_key=True)
    start_letter = models.CharField(max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    words = models.TextField(max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    end_letter = models.CharField(max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'unique_word'
'''

class Demo(models.Model):
    id = models.IntegerField(primary_key=True)
    start_letter = models.TextField(blank=True, null=True)
    words = models.TextField(blank=True, null=True)
    end_letter = models.TextField(blank=True, null=True)
    length = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'demo'
'''
