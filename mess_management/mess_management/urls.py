"""mess_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
import mainApp.views
import login.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^welcome/', login.views.welcome, name='welcome'),
    url(r'^loginStudent/', login.views.loginStudent, name='loginStudent'),
    url(r'^loginMessAuthority/', login.views.loginMessAuthority, name='loginMessAuthority'),
    url(r'^logout/', login.views.logout, name='logout'),
    url(r'^home/', mainApp.views.home, name='home'),
    url(r'^profile/', mainApp.views.profile, name='profile'),
    url(r'^tempOpt/', mainApp.views.tempOpt, name='tempOpt'),
    url(r'^viewOpt/', mainApp.views.viewOpt, name='viewOpt'),    
    url(r'^deleteOpt/', mainApp.views.deleteOpt, name='deleteOpt'),   
    url(r'^holiday/', mainApp.views.holiday, name='holiday'),
    url(r'^showDaysMenu/', mainApp.views.showDaysMenu, name='showDaysMenu'),
    url(r'^showWeeksMenu/', mainApp.views.showWeeksMenu, name='showWeeksMenu'),
    url(r'^reviewAndRate/', mainApp.views.reviewAndRate, name='reviewAndRate'),
    url(r'^account/', mainApp.views.account, name='account'),
    url(r'^stats/', mainApp.views.dispStats, name='stats'),
    url(r'^', login.views.welcome),
    url(r'^reg/', mainApp.views.reg, name='reg'),

]
