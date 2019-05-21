
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^restpassword/(?P<id>[\w-]+)', views.ResetPassword, name="reset"),
]
