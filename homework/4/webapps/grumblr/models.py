from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Entry(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    age = models.IntegerField(default="99", blank=True)
    bio = models.CharField(max_length=420, default="the user does not want to say anything", blank=True)
    picture = models.ImageField(upload_to="profile-photos", blank=True)
    def __str__(self):
        return self.firstname + " " + self.lastname

    @staticmethod
    def get_entries(owner):
        return Entry.objects.filter(owner=owner).first()#.order_by('lastname', 'firstname')

class Person(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    # name = models.CharField(max_length=20)
    relationships = models.ManyToManyField('self', related_name='related_to', through='Relationship',symmetrical=False)

    def get_follow(self):
        return self.relationships.filter(to_who__from_person=self)


class Relationship(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_who',on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_who',on_delete=models.CASCADE)

    def add_follow(self, person):
        relationship = Relationship(from_person=self, to_person=person)
        # relationship.save()
        return relationship

    def remove_follow(self, person):
        Relationship.objects.filter(from_person=self, to_person=person).delete()
        return




		