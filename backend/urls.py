from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login.as_view()),
    path('analysis/',views.analysis.as_view()),
    path('add/',views.addcomment.as_view()),
    path('add/<int:pk>/',views.Update_delete_comment.as_view()),
    path('adduser/',views.adduser.as_view()),
    path('addrestro/',views.addRestro.as_view()),
    path('top10/',views.leaderboard_view),
    path('allRestro/',views.allRestro.as_view()),
]