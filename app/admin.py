from django.contrib import admin
from .models import Emotion, Theme, Surrounding, Place, MoodEntry, HabitEntry, Habit, DiaryEntry

@admin.register(Emotion)
class EmotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    list_filter = ('type',)
    search_fields = ('name', 'description')

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('name', 'user')

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Surrounding)
class SurroundingAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'get_emotions')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'description')

    def get_emotions(self, obj):
        return ", ".join([emotion.name for emotion in obj.emotions.all()])
    get_emotions.short_description = 'Emotions'

@admin.register(HabitEntry)
class HabitEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'habit', 'start_time', 'end_time', 'duration_minutes')
    list_filter = ('habit', 'start_time', 'end_time', 'duration_minutes')
    search_fields = ('user__username', 'habit', 'description')

@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_truncated_body', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'body')

    def get_truncated_body(self, obj):
        return (obj.body[:88] + '...') if len(obj.body) > 88 else obj.body
    get_truncated_body.short_description = 'Body'