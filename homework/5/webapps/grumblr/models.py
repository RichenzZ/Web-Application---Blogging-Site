from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.utils.html import escape

class Item(models.Model):
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    last_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
     # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Item.objects.filter(last_changed__gt=time).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_items(time="1970-01-01T00:00+00:00"):
        return Item.objects.filter(last_changed__gt=time).distinct()

    @staticmethod
    def get_max_time():
        return Item.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

    @property
    def html(self):
        return """<div id='item_%d' class='well'><div class='row'><div class='col-sm-2'><p><a href='/view_profile/%d'> %s </a></p><img src='/photo/%d' class='img-circle' height='55' width='55'></div> <div class='col-sm-10'><p>%s<br>%s</p></div></div><p>Comments:</p><input type='text' name='comment' class='comment' id='%d' placeholder='Add your comments!' size='35'><button type='submit' class='comment-add'>Add</button></div>""" % (self.pk, self.user.id, escape(self.user.username), self.user.id, escape(self.date), escape(self.text), self.pk)


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
        return self.text

    @property
    def html(self):
        return """<div class='row'><div class='col-sm-1'></div><div class='col-sm-2'><p><a href='/view_profile/%d'>%s</a></p><img src='/photo/%d' class='img-circle' height='40' width='40'></div><div class='col-sm-9'><p>%s<br>%s</p></div></div>""" % (self.user.id, escape(self.user.username), self.user.id, escape(self.date), escape(self.text))



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





		
