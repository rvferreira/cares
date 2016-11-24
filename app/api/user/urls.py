from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.UserList.as_view()),
    url(r'^(?P<user_id>[0-9]+)/enrollment/$', views.EnrollmentList.as_view()),
    url(r'^enrollment/$', views.get_all_enrollments),
    url(r'^(?P<pk>[0-9]+)/$', views.UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)