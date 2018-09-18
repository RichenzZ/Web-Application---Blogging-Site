from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    # firstname = models.CharField(max_length=20)
    # lastname = models.CharField(max_length=20)
    # password = models.CharField(max_length=20)
    # username = models.CharField(max_length=20)
    # email = models.EmailField()

    # date = models.DateField(_("Date"), default=datetime.date.today)
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.text
		