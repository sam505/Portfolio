from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("create/information", views.form_create_view, name="information"),
    path("create/education", views.form_create_education_view, name="education"),
    path("create/experience", views.form_create_experience_view, name="experience"),
    path("create/skillset", views.form_create_skillset_view, name="skillset"),
    path("create/project", views.form_create_project_view, name="project"),
    path("api/<str:username>", views.api_view, name="api"),
    path("<str:username>", views.portfolio_view, name="portfolio")
]