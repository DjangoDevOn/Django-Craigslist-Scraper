from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('csv/', download_csv, name="csv"),
    path('get-craigslist-prospects', get_craigslist_prospects, name="get-craigslist-prospects"),
    path('user', login_required(user), name="user"),
    path('search/', SearchView.as_view(), name='search-results'),
    path('contacted/<int:pk>', login_required(contacted), name="contacted"),
    path('delete/<int:pk>', delete, name="delete"),
    # login
    path("login/", signin, name="login"),
    path("signout/", signout, name="signout"),
    path('signup/', UserSignupView.as_view(), name='signup'),
]
