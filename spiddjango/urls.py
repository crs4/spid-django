import django
from django.conf.urls import url
from djangosaml2 import views as djangosaml_views
from spiddjango import views as spid_views

urlpatterns = [
    url(r'^login/$', spid_views.login, name='spid_login'),
    url(r'^acs/$', djangosaml_views.assertion_consumer_service, name='spid_acs'),
    url(r'^logout/$', djangosaml_views.logout, name='saml2_logout'),
    url(r'^ls/$', djangosaml_views.logout_service, name='saml2_ls'),
    url(r'^ls/post/$', djangosaml_views.logout_service_post, name='saml2_ls_post'),
    url(r'^metadata/$', djangosaml_views.metadata, name='saml2_metadata'),
]