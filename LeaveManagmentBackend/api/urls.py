from django.urls import include, path
from .views import AccountView


urlpatterns = [
    path("account/", AccountView.as_view()),
	path('account/test/', AccountView.test),
]
