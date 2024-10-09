from django.urls import path

from .views import MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Custom token view for login
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),  # Custom refresh token view
]
