from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # shows if they've been contacted
    contacted = models.BooleanField(default=False)
    # lets you hide it but not delete it so you can do unique=true
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Prospect(models.Model):
    # unique is true so we can always rescrape and take new ones but not ones we already have
    settings = models.ManyToManyField(Settings)
    # simply for the one feature: toggling the checkmark on dashboard
    users = models.ManyToManyField(User)
    link = models.CharField(max_length=100, null=True, unique=True)
    post_title = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return self.link
 