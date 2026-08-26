"""rotebeete URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
import juntagrico

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^", include("juntagrico.urls")),
    path("", include("rotebeete.exports.urls")),
    path("", include("rotebeete.transitions.urls")),
    re_path(r"^$", juntagrico.views.home),
    re_path(r"^impersonate/", include("impersonate.urls")),
    re_path("djrichtextfield/", include("djrichtextfield.urls")),
    #re_path("admin/defender/", include("defender.urls")),
    re_path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("rb/biddinground/", include("biddings.urls")),
]
