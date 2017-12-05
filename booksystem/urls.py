"""booksystem URL Configuration

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
from booksmanage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/', views.index),
    url(r'^login/', views.logininterface),
    url(r'^logout/', views.logout_view),
    url(r'^signup/', views.register),
    url(r'^publisher/index/', views.publisherindex,name='publisherindex'),
    url(r'^author/index/', views.authorindex,name='authorindex'),
    url(r'^addbook/', views.addbook,name='addbook'),
    url(r'^editrecords/', views.editrecords),
    url(r'^editauthor/', views.editauthor),
    url(r'^editpublisher/', views.editpublisher),
    url(r'^delrecords/', views.delrecords),
    url(r'^delpublisher/', views.delpublisher,name='delpublisher'),
    url(r'^delauthor/', views.delauthor,name='delauthor'),
    url(r'^addpublisher/', views.addpublisher),
    url(r'^addauthor/', views.addauthor),

    url(r'^changepassword/', views.changepassword),
    url(r'^searchbook/', views.searchbook),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
