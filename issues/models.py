from django.db import models
from django.utils import timezone
from enum import Enum
from django.contrib.auth.models import User
from projects.models import Project
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class IssueStatusChoices(Enum):
    CREATED = "CREATED"
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    CLOSED = "CLOSED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="%(class)ss_created", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="%(class)ss_owned", null=True, on_delete=models.SET_NULL, blank=True)
    users = models.ManyToManyField(User, related_name="%(class)ss_watched", blank=True)
    title = models.CharField(max_length=50)
    details = models.CharField(max_length=300)
    priority = models.IntegerField(null=False, default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    closed_on = models.DateTimeField(blank=True)
    status = models.CharField(default=IssueStatusChoices.CREATED, max_length=50, choices=IssueStatusChoices.choices())
    estimated_work_hours = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    loaded_work_hours = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return 'Issue ' + str(self.title) + ' created by ' + str(self.creator.username)

    def get_absolute_url(self):
        return reverse('issues:issue-detail', kwargs={'project_id': self.project.id, 'pk': self.pk})

    def save(self, **kwargs):
        self.project = kwargs.get('project')
        super().save()


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Comment ' + str(self.title) + ' created by ' + str(self.creator.username)
