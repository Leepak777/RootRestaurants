from django.urls import path, include

from . import views

app_name = "foodRoots"
urlpatterns = [
    path("", views.index, name="index"),
    path("/start", views.start, name="start"),
    path("/reset", views.reset, name="reset"),
]
