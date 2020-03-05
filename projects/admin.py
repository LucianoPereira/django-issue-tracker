from django.contrib import admin
from projects.models import Project
from issues.models import Issue
from .models import Project


class IssueInline(admin.TabularInline):
    model = Issue
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = [IssueInline]
    search_fields = ['title', 'created_on']
    list_display = ('description', 'created_on', 'estimated_work_hours')


admin.site.register(Project, ProjectAdmin)