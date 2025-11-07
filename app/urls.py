from . import views
from django.urls import path


urlpatterns = [
    # landing routes
    path('', views.home, name="home"),
    path('signup', views.register, name="register"),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name="logout"),

    # diary routes
    path('diary', views.diary, name="diary"),
    path('diary/write', views.write_diary, name="write_diary"),
    path('diary/<int:entry_id>/', views.diary_detail, name='diary_detail'),
    path('diary/<int:entry_id>/delete/', views.delete_diary_entry, name='delete_diary_entry'),
    path('diary/<int:entry_id>/update/', views.update_diary_entry, name='update_diary_entry'),

    # mood routes
    path('mood', views.mood_home, name='mood_home'),
    path('mood/check-in', views.mood_check_in, name='mood_checkin'),
    path('mood/<int:entry_id>/', views.mood_detail, name='mood_detail'),
    path('mood/<int:entry_id>/delete/', views.delete_mood_entry, name='delete_mood'),

    # habit routes
    path('habits', views.habit_tracking, name="habits"),
    path('habits/add', views.add_habit_entry, name="add_habit_entry"),
    path('habits/<int:entry_id>/', views.habit_detail, name='habit_detail'),
    path('habits/<int:entry_id>/delete/', views.delete_habit_entry, name='delete_habit_entry'),
    path('habits/<int:entry_id>/update/', views.update_habit_entry, name='update_habit_entry'),
]