from django.contrib import admin
from django.urls import include, path
from dashboard.views import *

urlpatterns = [
    path('', include('login.urls')),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('dashboard', dashView.as_view(), name='dashboard'),
]
