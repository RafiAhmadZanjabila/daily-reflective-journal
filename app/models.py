from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Emotion(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.TextField()
    TYPE_CHOICES = [
        ('HEU', 'High Energy Unpleasant'),
        ('LEU', 'Low Energy Unpleasant'),
        ('LEP', 'Low Energy Pleasant'),
        ('HEP', 'High Energy Pleasant'),
    ]
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name}"

class Theme(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.name}"

class Surrounding(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"

class Place(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"

class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    emotions = models.ManyToManyField(Emotion, related_name='mood_entries')
    themes = models.ManyToManyField(Theme, blank=True, related_name='mood_entries')
    surroundings = models.ManyToManyField(Surrounding, blank=True, related_name='mood_entries')
    places = models.ManyToManyField(Place, blank=True, related_name='mood_entries')
    description = models.TextField()
    created_at = models.DateTimeField(default=now)
    sleep_time = models.PositiveIntegerField(default=0)
    exercise_minutes = models.PositiveIntegerField(default=0)
    steps = models.PositiveIntegerField(default=0)
    temperature = models.PositiveIntegerField(blank=False, null=False)
    weather_condition = models.CharField(blank=False, null=False, max_length=20) 

class Habit(models.Model):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')

    def __str__(self):
        return f"{self.name}"

class HabitEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habit_entries')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='entries')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.IntegerField(editable=False)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        duration = self.end_time - self.start_time
        self.duration_minutes = int(duration.total_seconds() // 60)
        super().save(*args, **kwargs)

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    body = models.TextField()
    created_at = models.DateTimeField(default=now)
