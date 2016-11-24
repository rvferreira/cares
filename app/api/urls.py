from django.conf.urls import url, include
from . import login, logout, signup

urlpatterns = [
    url(r'^login/$', login.handler),
    url(r'^logout/$', logout.handler),
    url(r'^signup/$', signup.handler),
    url(r'^user/', include('app.api.user.urls')),
    url(r'^career/', include('app.api.career.urls')),
    url(r'^ticket/', include('app.api.ticket.urls')),
    url(r'^sprint/', include('app.api.sprint.urls')),
]