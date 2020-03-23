from django.contrib.auth.models import User


def latest_users(request):
    try:
        users = User.objects.all().order_by('-date_joined')[:5]
        last_users = {'latest_users': users}
        return last_users
    finally:
        pass
    raise ValueError("Not enough users to show")
