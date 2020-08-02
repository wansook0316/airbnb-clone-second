"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings  # 장고에서 settings.py를 import할 때는 이와 같은 방식으로 한다.
from django.conf.urls.static import static


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    # path("users", include("users.urls", namespace="users")),
    path("admin/", admin.site.urls),
]

# 개발 모드인지 확인하고, 파일을 제공한다. 아닌 경우는 보안상 하면 안돼
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # settings.MEDIA_URL(media)로 요청이 들어오면, settings.MEDIA_ROOT(/uploads)로 보낸다.
