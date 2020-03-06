from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from projects.models import Project
from .models import Issue
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class IssueDetailView(DetailView):
    model = Issue


class UserIssueListView(ListView):
    model = Issue
    ordering = ['-created_on']
    template_name = 'issues/user_issues.html'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Issue.objects.filter(creator=user).order_by('-created_on')


class ProjectIssueListView(ListView):
    model = Issue
    ordering = ['-created_on']
    template_name = 'issues/project_issues.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectIssueListView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs.get('project_id'))
        return context

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
        return Issue.objects.filter(project=project).order_by('-created_on')


class IssueCreateView(LoginRequiredMixin, CreateView):
        model = Issue
        fields = ['title', 'details', 'priority', 'status', 'estimated_work_hours', 'loaded_work_hours']

        def form_valid(self, form):
            form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
            form.instance.creator = self.request.user
            return super().form_valid(form)


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['title', 'details', 'priority', 'status', 'estimated_work_hours', 'loaded_work_hours']

    def test_func(self):
        issue = self.get_object()
        if self.request.user == issue.creator:
            return True
        return False


class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue

    def test_func(self):
        issue = self.get_object()
        if self.request.user == issue.creator:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.object.project.pk})


def about(request):
    return render(request, 'issues/about.html', {'title': 'about'})
