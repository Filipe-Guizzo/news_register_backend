from django.db import models
from person.models import Person
from category.models import Category

class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='', blank=True, null=True, default='default.png')
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category')
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='id_person')
    dt_create = models.DateField(auto_now_add=True)
    dt_update = models.DateField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'news'
