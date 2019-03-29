"""testsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts import views as accounts_views
from tests import views as tests_views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', tests_views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^\w*/*login/$',
        auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^test_view/(\d+)/$', tests_views.test_view, name='test_view'),
    url(r'^test_view/(\d+)/new_comment$',
        tests_views.new_comment, name='new_comment'),
    url(r'^test_create/$', tests_views.test_create, name='test_create'),
    url(r'^account/$', accounts_views.save_profile, name='my_account'),
    url(r'^test_list/(\d+)/$', tests_views.test_list, name='test_list'),
    url(r'^test_result/$', tests_views.test_result, name='test_result'),
    url(r'^all_tests/$', tests_views.all_tests, name='all_tests'),
    url(r'^test_upload$', tests_views.test_json, name='test_json'),
    #url(r'^test_list/(\d+)/$', tests_views.TestListView.as_view(template_name='test_list.html'), name='test_list'),
    #url(r'^signup/$', accounts_views.signup, name='signup'),
    #url(r'^tests/$', tests_views.tests, name='tests' ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
