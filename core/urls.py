from rest_framework import routers
from core import views

router = routers.DefaultRouter()

router.register('categories', views.CategoryViewSet, basename='categories')
router.register('products', views.ProductViewSet, basename='products')
router.register('cart', views.CartViewSet, basename='cart')
router.register('reviews', views.ReviewViewSet, basename='reviews')
router.register('favourites', views.FavouriteViewSet, basename='favourites')
router.register('orders', views.OrderViewSet, basename='orders')

urlpatterns = router.urls
