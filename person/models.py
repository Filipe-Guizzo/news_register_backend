from django.db import models
class Person(models.Model):
    SEX_CHOICES = (
        ('M', 'Masculine'),
        ('F', 'Feminine')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    date_born = models.DateField()
    sex = models.CharField(max_length=1, blank=True, null=True, choices=SEX_CHOICES)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=500)
    photo = models.ImageField(upload_to="", blank=True, null=True, default='default.png')
    dt_create = models.DateField(auto_created=True, auto_now_add=True, blank=True, null=True)
    dt_update = models.DateField(auto_created=True, auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'
