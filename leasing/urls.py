"""leasing URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static
from django.conf import settings
import leasingapi.urls


urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-docs/', include_docs_urls(title='Leasing API Docs')),
    url(r'^api/v1/', include('leasingapi.urls', namespace="leasingapi")),
    url(r'^email/', include('leasingmail.urls'))
    # ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
