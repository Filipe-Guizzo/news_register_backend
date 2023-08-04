from django.db import models
from person.models import Person

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='id_person')
    dt_create = models.DateField(auto_now_add=True)
    dt_update = models.DateField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'category'
