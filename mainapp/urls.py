from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiscountViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'discounts', DiscountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # for getting the JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # for refreshing the JWT
]
