from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Project(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Project ' + str(self.title) + ' created by ' + str(self.creator.username)

    def estimated_work_hours(self):
        total = 0
        sum_hours = sum([issue.estimated_work_hours for issue in self.issue_set.all()])
        if sum_hours == 0:
            raise ValueError("The estimated total work hours in this project are equal to 0")
        return sum_hours

    def loaded_work_hours(self):
        return sum([issue.loaded_work_hours for issue in self.issue_set.all()])

    def progress_percentage(self):
        try:
            progress = int((self.loaded_work_hours() / self.estimated_work_hours()) * 100)
            if progress < 100:
                return progress
            return 100
        except ValueError:
            return 0

    def project_issues_status(self):
        status_count = {}
        for issue in self.issue_set.all():
            if issue.status in status_count:
                status_count[issue.status] += 1
            else:
                status_count[issue.status] = 1
        return status_count

    def get_absolute_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.pk})

