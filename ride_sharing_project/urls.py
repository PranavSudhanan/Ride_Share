from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from users.views import UserRegisterViewSet
from rides.views import RideStatusUpdateViewSet, RideTrackingViewSet, RideViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()

# User endpoints
router.register(r'register', UserRegisterViewSet, basename='register')

# Ride endpoints
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'rides/status', RideStatusUpdateViewSet, basename='ride-status')
router.register(r'rides/tracking', RideTrackingViewSet, basename='ride-tracking')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

