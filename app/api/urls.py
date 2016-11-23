from django.conf.urls import url, include
from . import login

urlpatterns = [
    url(r'^login/$', login.handler),
    url(r'^user/', include('app.api.user.urls')),

]