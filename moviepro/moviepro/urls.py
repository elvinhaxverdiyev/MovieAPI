from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Movie API",
      default_version='v1',
      description="Movie API documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@moviepro.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),  
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("apis.urls")),  
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'), 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

