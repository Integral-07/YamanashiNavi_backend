from django.urls import path
from . import views

"""
from .views import LoginView

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)
"""

urlpatterns = [

    path('', views.conversation),
    path('login/', views.login),
    path('signup/', views.Signup),
    path('chat/<user_id>', views.conversation)
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]