from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from .models import DiaryEntry, Habit, HabitEntry, Emotion, Theme, Surrounding, Place, MoodEntry
from django.views.decorators.http import require_POST
import json

from .utils import get_emotion_color


def home(request):
    if not request.user.is_authenticated:
        return render(request, "app/home.html")
    else:
        today = date.today()
        mood_count = request.user.mood_entries.filter(created_at__date=today).count()
        habit_count = request.user.habit_entries.filter(start_time__date=today).count()
        diary_count = request.user.diary_entries.filter(created_at__date=today).count()
        context = {
            'mood_count': mood_count,
            'habit_count': habit_count,
            'diary_count': diary_count,
            'first_name': request.user.first_name,
        }
        return render(request, "app/app.html", context)
        

def register(request):
    if request.method == 'GET':
        return render(request, 'app/register.html')
    
    first = request.POST.get('firstName', '')
    if not first:
        return render(request, 'app/register.html', {
            'message': "First name required"
        })

    last = request.POST.get('lastName', '')

    password = request.POST.get('password', '')
    confirmation = request.POST.get('confirmpassword', '')
    if password != confirmation:
        return render(request, 'app/register.html', {
            'message': "Passwords must match"
        })
    
    username = request.POST.get('username', '')
    try:
        user = User.objects.create_user(username=username, password=password, first_name=first, last_name=last)
        user.save()
    except IntegrityError:
        return render(request, 'app/register.html', {
            'message': "Username already exists"
        })
    login(request, user)
    return HttpResponseRedirect(reverse('home'))


def login_user(request):
    if request.method == 'GET':
        return render(request, 'app/login.html')
    
    user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "app/login.html", {
            "message": "Invalid username and/or password"
        })


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse("home"))
    return HttpResponse(status=403)


@login_required
def diary(request):
    today = date.today()
    today_entries = request.user.diary_entries.filter(created_at__date=today).order_by('-created_at')
    past_entries = request.user.diary_entries.exclude(created_at__date=today).order_by('-created_at')
    context = {
        'today_entries': today_entries,
        'past_entries': past_entries,
    }
    return render(request, "app/diaryhome.html", context)

@login_required
def write_diary(request):
    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if not body:
            return render(request, "app/writediary.html", {
                'error_message': "Diary entry cannot be empty."
            })
        DiaryEntry.objects.create(user=request.user, body=body)
        return redirect('diary')
    return render(request, "app/writediary.html")


@login_required
def diary_detail(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    context = {
        'entry': entry,
    }
    return render(request, 'app/diary_detail.html', context)

@login_required
@require_POST
def delete_diary_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    entry.delete()
    return JsonResponse({'success': True})

@login_required
@require_POST
def update_diary_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    body = request.POST.get('body', '').strip()
    if not body:
        return JsonResponse({'success': False, 'error': "Diary entry cannot be empty."})
    entry.body = body
    entry.save()
    return JsonResponse({'success': True, 'body': entry.body})

@login_required
def habit_tracking(request):
    today = date.today()

    active = 0
    today_entries = request.user.habit_entries.filter(
        start_time__date=today
    ).order_by('-start_time')
    for entry in today_entries:
        active += entry.duration_minutes

    past_entries = request.user.habit_entries.exclude(
        start_time__date=today
    ).order_by('-start_time')

    context = {
        'today_entries': today_entries,
        'past_entries': past_entries,
        'active': active
    }
    
    return render(request, "app/habit_home.html", context)

@login_required
def add_habit_entry(request):
    if request.method == 'POST':
        habit_name = request.POST.get('habit_name', '').strip()
        habit_id = request.POST.get('habit_id', '')
        description = request.POST.get('description', '').strip()
        start_time_str = request.POST.get('start_time', '')
        end_time_str = request.POST.get('end_time', '')
        if not (start_time_str and end_time_str):
            return JsonResponse({'success': False, 'error': "Start time and end time are required."})
        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            return JsonResponse({'success': False, 'error': "Invalid date format."})
        if start_time >= end_time:
            return JsonResponse({'success': False, 'error': "End time must be after start time."})
        if habit_name:
            habit, _ = Habit.objects.get_or_create(name=habit_name, user=request.user)
        elif habit_id:
            habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        else:
            return JsonResponse({'success': False, 'error': "Please select or add a habit."})
        HabitEntry.objects.create(
            user=request.user,
            habit=habit,
            start_time=start_time,
            end_time=end_time,
            description=description,
        )
        return JsonResponse({'success': True})
    else:
        habits = request.user.habits.all()
        return render(request, "app/add_habit_entry.html", {'habits': habits})

@login_required
def habit_detail(request, entry_id):
    entry = get_object_or_404(HabitEntry, id=entry_id, user=request.user)
    context = {
        'entry': entry,
    }
    return render(request, 'app/habit_detail.html', context)

@login_required
@require_POST
def delete_habit_entry(request, entry_id):
    entry = get_object_or_404(HabitEntry, id=entry_id, user=request.user)
    entry.delete()
    return JsonResponse({'success': True})

@login_required
@require_POST
def update_habit_entry(request, entry_id):
    entry = get_object_or_404(HabitEntry, id=entry_id, user=request.user)
    description = request.POST.get('description', '').strip()
    start_time_str = request.POST.get('start_time', '')
    end_time_str = request.POST.get('end_time', '')
    if not (start_time_str and end_time_str):
        return JsonResponse({'success': False, 'error': "Start time and end time are required."})
    start_time = datetime.fromisoformat(start_time_str)
    end_time = datetime.fromisoformat(end_time_str)
    if start_time >= end_time:
        return JsonResponse({'success': False, 'error': "End time must be after start time."})
    entry.start_time = start_time
    entry.end_time = end_time
    entry.description = description
    entry.save()
    return JsonResponse({'success': True})

@login_required
def mood_check_in(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        emotion_id = data.get('emotion_id')
        themes = data.get('themes', [])
        places = data.get('places', [])
        surroundings = data.get('surroundings', [])
        description = data.get('description', '').strip()
        sleep_time = data.get('sleep_time')
        exercise_minutes = data.get('exercise_minutes')
        steps = data.get('steps')
        temperature = data.get('temperature')
        weather_condition = data.get('weather_condition')
        created_at_str = data.get('created_at')
        if created_at_str:
            created_at = datetime.fromisoformat(created_at_str)
        else:
            created_at = timezone.now()

        mood_entry = MoodEntry.objects.create(
            user=request.user,
            description=description,
            sleep_time=sleep_time,
            exercise_minutes=exercise_minutes,
            steps=steps,
            temperature=temperature,
            weather_condition=weather_condition,
            created_at=created_at,
        )
        if emotion_id:
            emotion = get_object_or_404(Emotion, id=emotion_id)
            mood_entry.emotions.add(emotion)
        for theme_id in themes:
            theme = get_object_or_404(Theme, id=theme_id)
            mood_entry.themes.add(theme)
        for place_id in places:
            place = get_object_or_404(Place, id=place_id)
            mood_entry.places.add(place)
        for surrounding_id in surroundings:
            surrounding = get_object_or_404(Surrounding, id=surrounding_id)
            mood_entry.surroundings.add(surrounding)

        return JsonResponse({'success': True})
    else:
        emotions = Emotion.objects.all()
        themes = Theme.objects.all()
        places = Place.objects.all()
        surroundings = Surrounding.objects.all()
        context = {
            'emotions': emotions,
            'themes': themes,
            'places': places,
            'surroundings': surroundings,
        }
        return render(request, 'app/add_mood.html', context)

@login_required
def mood_home(request):
    today = date.today()
    today_entry = request.user.mood_entries.filter(created_at__date=today).order_by('-created_at')
    for entry in today_entry:
        if entry.emotions.exists():
            emotion = entry.emotions.first()
            emotion_type = emotion.type
            emotion_color = get_emotion_color(emotion_type)
            entry.emotion = emotion
            entry.emotion_color = emotion_color
    past_entries = request.user.mood_entries.exclude(created_at__date=today).order_by('-created_at')
    for entry in past_entries:
        if entry.emotions.exists():
            emotion = entry.emotions.first()
            emotion_type = emotion.type
            emotion_color = get_emotion_color(emotion_type)
            entry.emotion = emotion
            entry.emotion_color = emotion_color
    context = {
        'today_entry': today_entry,
        'past_entries': past_entries,
    }
    return render(request, "app/mood_home.html", context)

@login_required
def mood_detail(request, entry_id):
    entry = get_object_or_404(MoodEntry, id=entry_id, user=request.user)
    if entry.emotions.exists():
        emotion = entry.emotions.first()
        emotion_type = emotion.type
        emotion_color = get_emotion_color(emotion_type)
        entry.emotion = emotion
        entry.emotion_color = emotion_color
    context = {
        'entry': entry,
    }
    return render(request, 'app/mood_detail.html', context)

@login_required
@require_POST
def delete_mood_entry(request, entry_id):
    entry = get_object_or_404(MoodEntry, id=entry_id, user=request.user)
    entry.delete()
    return JsonResponse({'success': True})
