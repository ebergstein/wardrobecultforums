from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = "home"),
    url(r'^register/', views.register, name = "register"),
    url(r'^login/', views.login, name = "login"),
    url(r'^forgot/', views.forgot, name = "forgot"),
    url(r'^(?P<first>\w+)/(?P<last>\w+)/(?P<email>[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+)/(?P<password>\w+)/$', views.auto, name= "redirect")
]
