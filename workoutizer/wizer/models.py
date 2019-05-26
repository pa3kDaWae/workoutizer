from django.db import models


class Sport(models.Model):

    def __str__(self):
        return self.sport

    sport = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=200, unique=True)


class Activity(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=400)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.IntegerField()
    distance = models.IntegerField()
