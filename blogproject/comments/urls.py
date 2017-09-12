from django.conf.urls import url
from . import views

# regular expression
app_name = 'comment'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='comments'),
]