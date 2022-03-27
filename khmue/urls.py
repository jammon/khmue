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
from geraete import views as g_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", g_views.index),
    path("mitarbeiter/", g_views.employees, name="employees"),
    path("mitarbeiter/<int:id>", g_views.employee_edit),
    path("geraete", g_views.devices),
    path("geraete/add", g_views.device_add),
    path("gruppen", g_views.prof_groups, name="prof_groups"),
    path("gruppen/add", g_views.prof_group, name="prof_group_add"),
    path("gruppen/<int:id>", g_views.prof_group, name="prof_groups_edit"),
    path("einweisung", g_views.instruction),
    path("ersteinweisungen", g_views.primaryinstructions),
    path("ersteinweisung/<int:id>", g_views.primaryinstruction),
    path(
        "ersteinweisung", g_views.primaryinstruction, name="primaryinstruction"
    ),
    path("get_devices", g_views.get_devices, name="get_devices"),
    path("lacking", g_views.lacking_instructions, name="lacking"),
    path("pass/<int:employee_id>", g_views.get_cert, name="get_cert"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
