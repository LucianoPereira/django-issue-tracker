from django.urls import path
from . import views
from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    UserProjectListView
)

app_name = 'projects'
urlpatterns = [
    path('', ProjectListView.as_view(), name='home'),
    path('user/<str:username>/', UserProjectListView.as_view(), name='user-projects'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('new/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('about/', views.about, name='about'),
]
