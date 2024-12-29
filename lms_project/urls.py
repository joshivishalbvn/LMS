from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from app_modules.users.views import DashboardView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("accounts/", include("allauth.urls")),
    path('accounts/', include('allauth.socialaccount.urls')),
    path("users/", include("app_modules.users.urls")),
    path("courses/", include("app_modules.course.urls")),
    path("",DashboardView.as_view(), name="dashboard"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

