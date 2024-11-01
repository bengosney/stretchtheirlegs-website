from django.urls import path

from site_messages import views

app_name = "site_messages"
urlpatterns = [
    path("dismiss/<slug:slug>", views.dismiss, name="dismiss"),
]
