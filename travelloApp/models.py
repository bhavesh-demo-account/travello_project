from django.db import models

# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='static/pics')
    desc = models.TextField()
    price = models.IntegerField()
    offers = models.BooleanField(default=False)
    def __str__(self):
         return f'{self.name}'
