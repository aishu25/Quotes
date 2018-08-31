from django.conf.urls import url
from . import views           
urlpatterns = [
url(r'^$',views.index),
url(r'^logval$',views.logval),
url(r'^regval$',views.regval),
url(r'^quotes$',views.show_quotes),
url(r'^allquote$',views.allquote_add),
url(r'^removefq/(?P<id>\d+)$',views.removefq),
url(r'^addfq/(?P<id>\d+)$',views.addfq),
url(r'^users/(?P<id>\d+)$',views.show_user),
url(r'^logout$',views.logoutpage),
]