"""contact_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from contacts.views import UserViewSet, ContactViewSet, AddContactForUser, UserConatctView, SignupView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'user/contacts', UserConatctView, basename='user-contacts-list')
# router.register(r'signup', )

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^contact/add/', AddContactForUser.as_view(), name='c'),
    re_path(r'^signup/', SignupView.as_view(), name='signup'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)