from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/auto-show/', include('Auto_Show.urls')),
    path('api/users/', include('Users.urls')),

]+ debug_toolbar_urls()


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )