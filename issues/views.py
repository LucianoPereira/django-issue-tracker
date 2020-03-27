from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from projects.models import Project
from .models import Issue, IssueStatusChoices
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import IssueForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect


class IssueDetailView(UserPassesTestMixin, DetailView):
    model = Issue

    def test_func(self):
        if self.request.user in self.get_object().users.all() \
                or self.request.user == self.get_object().creator \
                or self.request.user == self.get_object().owner:
            return True
        return False


class UserIssueListView(ListView):
    model = Issue
    ordering = ['-created_on']
    template_name = 'issues/user_issues.html'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Issue.objects.filter(owner=user).order_by('-created_on')


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
    form_class = IssueForm

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        form.instance.creator = self.request.user

        return super().form_valid(form)


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    form_class = IssueForm

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
        return reverse_lazy('issues:project-issues', kwargs={'project_id': self.object.project.pk})


def ownership_view(request, project_id, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if not issue.owner:
        if request.method == "POST":
            issue.owner = request.user
            issue.status = IssueStatusChoices.ASSIGNED.value
            issue.save()
            messages.info(request, 'You have taken ownership successfully')
            return HttpResponseRedirect(
                reverse_lazy('issues:issue-detail', kwargs={'project_id': project_id, 'pk': pk}))
        else:
            context = {}
            context['project_id'] = project_id
            context['pk'] = pk
            context['issue'] = issue
            return render(request, 'issues/confirm_ownership.html', context)
    else:
        messages.warning(request, 'This issue already has an owner')
    return HttpResponseRedirect(reverse_lazy('issues:project-issues', kwargs={'project_id': project_id}))


def load_hours_view(request, project_id, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == "POST":
        if request.user == issue.owner:
            input_hours = int(request.POST.get('hours'))
            if input_hours >= 0:
                issue.loaded_work_hours += input_hours
                issue.save()
                messages.info(request, "You have loaded hours to this Issue")
            else:
                messages.warning(request, "You can't load negative hours")
        else:
            messages.warning(request, "You can't load hours if you are not the issue's owner")
        return HttpResponseRedirect(reverse_lazy('issues:issue-detail', kwargs={'project_id': project_id, 'pk': pk}))
    else:
        context = {}
        context['project_id'] = project_id
        context['pk'] = pk
        context['issue'] = issue
    return render(request, "issues/issue_confirm_load_hours.html", context)


def about(request):
    return render(request, 'issues/about.html', {'title': 'about'})
