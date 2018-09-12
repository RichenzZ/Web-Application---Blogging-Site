from django.db import models

# Create your models here.

class student(models.Model):
    andrewid = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)

    def __str__(self):
        return self.andrewid, self.firstname, self.lastname 

class course(models.Model):
    coursenum = models.CharField(max_length=200)
    coursename = models.CharField(max_length=200)
    courseins = models.CharField(max_length=200)

    def __str__(self):
        return self.coursenum, self.coursename, self.courseins
