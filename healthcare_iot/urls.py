from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from backend.views import UserViewSet, HospitalViewSet, UserRoleViewSet, CustomCreateView


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hospital', HospitalViewSet)
router.register(r'user-role', UserRoleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', CustomCreateView.as_view(), name='create_custom_objects'),
    path('api/', include(router.urls))
]
