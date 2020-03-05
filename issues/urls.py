from django.urls import path
from . import views
from .views import (
    IssueDetailView,
    IssueCreateView,
    IssueUpdateView,
    IssueDeleteView,
    UserIssueListView,
    ProjectIssueListView
)
app_name = 'issues'
urlpatterns = [
    path('projects/<int:project_id>/issues/', ProjectIssueListView.as_view(), name='project-issues'),
    path('<str:username>/issues/', UserIssueListView.as_view(), name='user-issues'),
    path('projects/<int:project_id>/issues/<int:pk>/', IssueDetailView.as_view(), name='issue-detail'),
    path('projects/<int:project_id>/issues/new/', IssueCreateView.as_view(), name='issue-create'),
    path('projects/<int:project_id>/issues/<int:pk>/update/', IssueUpdateView.as_view(), name='issue-update'),
    path('projects/<int:project_id>/issues/<int:pk>/delete/', IssueDeleteView.as_view(), name='issue-delete'),
]
