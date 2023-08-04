from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    id_person = models.ForeignKey('Person', models.DO_NOTHING, db_column='id_person')
    dt_create = models.DateField()
    dt_update = models.DateField()

    class Meta:
        managed = False
        db_table = 'category'


class News(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=150)
    photo = models.CharField(max_length=500, blank=True, null=True)
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category')
    id_person = models.ForeignKey('Person', models.DO_NOTHING, db_column='id_person')
    dt_create = models.DateField()
    dt_update = models.DateField()

    class Meta:
        managed = False
        db_table = 'news'


class Person(models.Model):
    name = models.CharField(max_length=50)
    date_born = models.DateField()
    sex = models.CharField(max_length=1, blank=True, null=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=500)
    photo = models.CharField(max_length=500, blank=True, null=True)
    dt_create = models.DateField()
    dt_update = models.DateField()

    class Meta:
        managed = False
        db_table = 'person'
