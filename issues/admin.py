from django.contrib import admin
from issues.models import Issue, Comment
admin.site.register(Issue)
admin.site.register(Comment)
