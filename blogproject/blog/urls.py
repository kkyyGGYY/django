from django.conf.urls import url

from . import views

# regular expression
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),  # as_view把IndexView变成一个视图函数
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesViews.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
]

# urlpatterns = [
#     url(r'^$',views.IndexView.as_view(),name='index'),
#     url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetailView.as_view(),name='detail'), # post/1
#     # archives/2017/9/
#     url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
#     url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
# ]