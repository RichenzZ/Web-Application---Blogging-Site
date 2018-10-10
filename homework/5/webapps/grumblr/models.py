from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Entry(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20, blank=True)
    lastname = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(blank=True)
    bio = models.CharField(max_length=420, default="the user does not want to say anything", blank=True)
    picture = models.ImageField(upload_to="profile-photos", blank=True)
    def __str__(self):
        return self.firstname + " " + self.lastname

    @staticmethod
    def get_entries(owner):
        return Entry.objects.filter(owner=owner).first()

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
	text = models.CharField(max_length=42)
	date = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.user + " " + self.text
		

class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    relationships = models.ManyToManyField('self', related_name='related_to', through='Relationship',symmetrical=False)
    
    def __str__(self):
        return self.user.username

    def get_follow(self):
        return self.relationships.filter(to_who__from_person=self)


class Relationship(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_who',on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_who',on_delete=models.CASCADE)

    def add_follow(self, person):
        relationship = Relationship(from_person=self, to_person=person)
        return relationship

    def remove_follow(self, person):
        Relationship.objects.filter(from_person=self, to_person=person).delete()
        return





		