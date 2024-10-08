from rest_framework import permissions
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

class MyTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)
