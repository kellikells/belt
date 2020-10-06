from django.conf.urls import url
from . import views         

urlpatterns = [
    url(r'^$', views.index, name='belt_app_index'),

 
    url(r'^register/$', views.register , name='belt_app_register'),

    url(r'^register_success/$', views.register_success , name='belt_app_register_success'),

    url(r'^logout/$', views.logout, name='belt_app_logout'),

    url(r'^login/$', views.login, name='belt_app_login'),

    url(r'^login_success/$', views.login_success, name='belt_app_login_success'),

    url(r'^addReview/(?P<id>\d+)/$', views.addReview, name='belt_app_addReview'),
    
    url(r'^addPage/$', views.addPage, name='belt_app_addPage'),

    url(r'^get_book_review/(?P<book_id>\d+)/$', views.get_book_review, name='belt_app_get_book_review'),

    url(r'^booksPage/$', views.booksPage, name='belt_app_booksPage'),
    
    url(r'^getUser/(?P<user_id>\d+)/$', views.getUser, name='belt_app_getUser'),

    url(r'^delete_review/(?P<book_id>\d+)/(?P<review_id>\d+)/$', views.delete_review, name='belt_app_delete_review'),

    url(r'^additionalReview/(?P<book_id>\d+)/$', views.additionalReview, name='belt_app_additionalReview'),

    # url(r'^/$', , name='belt_app_'),
    
    # url(r'^/$', , name='belt_app_'),

    # url(r'^/$', , name='belt_app_'),
    
    # url(r'^/$', , name='belt_app_'),
    
]