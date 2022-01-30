"""khmue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from geraete import views as geraete_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", geraete_views.index),
    path("mitarbeiter/", geraete_views.employees, name="employees"),
    path("mitarbeiter/<int:id>", geraete_views.employee_edit),
    path("geraete", geraete_views.devices),
    path("geraete/add", geraete_views.device_add),
    path("gruppen", geraete_views.prof_groups, name="prof_groups"),
    path("gruppen/add", geraete_views.prof_group),
    path("gruppen/<int:id>", geraete_views.prof_group),
    path("einweisung", geraete_views.instruction),
    path("ersteinweisung", geraete_views.primaryinstruction),
    path("get_devices", geraete_views.get_devices, name="get_devices"),
    path("lacking", geraete_views.lacking_instructions, name="lacking"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
