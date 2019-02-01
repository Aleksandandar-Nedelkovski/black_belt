from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_job$', views.add_job),
    url(r'^addjob$', views.addjob),
    url(r'^add_favorite/(?P<id>[0-9]+)$', views.add_favorite),
    url(r'^view/(?P<id>[0-9]+)$', views.view),
    url(r'^view/add_favorite/(?P<id>[0-9]+)$', views.add_favorite),
    url(r'^delete_fav/(?P<id>\d+)$', views.delete_fav),
    url(r'^edit/(?P<id>[0-9]+)$', views.edit),
    url(r'^edit/update_jobs/(?P<id>[0-9]+)$', views.update_jobs)
]