from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from auth_ import views

router = routers.DefaultRouter()

router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', views.register_user),
    path('confirm/', views.confirm_email),
    path('customer_profiles/<int:profile_id>/', views.CustomerProfileAPIView.as_view()),
    path('admin_profiles/<int:profile_id>/', views.AdminProfileAPIView.as_view()),
    path('brands/', views.BrandAPIView.as_view()),
    path('brands/<int:profile_id>/', views.BrandDetailsAPIView.as_view()),
]

urlpatterns += router.urls
