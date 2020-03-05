from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Project
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from projects import urls
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'projects/home.html', context)


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/home.html'
    context_object_name = 'projects'
    ordering = ['-created_on']
    paginate_by = 4


class UserProjectListView(ListView):
    model = Project
    template_name = 'projects/user_projects.html'
    context_object_name = 'projects'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Project.objects.filter(creator=user).order_by('-created_on')


class ProjectDetailView(DetailView):
    model = Project


class ProjectCreateView(LoginRequiredMixin, CreateView):
        model = Project
        fields = ['title', 'description', ]

        def form_valid(self, form):
            form.instance.creator = self.request.user
            return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'description', ]

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.creator:
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects:home')

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.creator:
            return True
        return False


def about(request):
    return render(request, 'projects/about.html', {'title': 'about'})
