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
    path("<str:username>", views.portfolio_view, name="portfolio"),

    path("update/information", views.form_update_view, name="update_information"),
    path("update/education", views.form_update_education_view, name="update_education"),
    path("update/experience", views.form_update_experience_view, name="update_experience"),
    path("update/skillset", views.form_update_skillset_view, name="update_skillset"),
    path("update/project", views.form_update_project_view, name="update_project"),

    path("delete/information/<int:id>", views.info_delete_view, name="delete_information"),
    path("delete/education/<int:id>", views.edu_delete_view, name="delete_education"),
    path("delete/experience/<int:id>", views.exp_delete_view, name="delete_experience"),
    path("delete/project/<int:id>", views.proj_delete_view, name="delete_project"),
    path("delete/skillset/<int:id>", views.skill_delete_view, name="delete_skillset"),
]