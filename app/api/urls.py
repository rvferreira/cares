from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import user

urlpatterns = [
    url(r'^user/$', user.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', user.UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)