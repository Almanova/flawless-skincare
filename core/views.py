from rest_framework import viewsets
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Category, Product, CartItem, Review, Favourite, \
    Order
from core.serializers import CategorySerializer, ProductSerializer, \
    ProductImageSerializer, CartItemSerializer, CartItemListSerializer, \
    ReviewSerializer, FavouriteSerializer, OrderSerializer
from utils import constants
from utils.filters import ProductFilter
from utils.parsers import MultipleFilesParser
from utils.permissions import AdminOnly, OwnerOnly

import logging

logger = logging.getLogger(__name__)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AdminOnly, ]


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AdminOnly, ]
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name',
                     'brand__name',
                     'category__name']

    @action(detail=True,
            methods=['post'],
            url_path='upload',
            parser_classes=[MultipleFilesParser])
    def upload(self, request, *args, **kwargs):
        instance = self.get_object()
        context = super().get_serializer_context()
        context['product'] = instance
        serializer = ProductImageSerializer(data=request.data,
                                            context=context,
                                            many=True)
        serializer.is_valid(raise_exception=True)
        uploaded = serializer.save()
        return Response(ProductImageSerializer(
            uploaded, many=True).data)


class CartViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [OwnerOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return CartItemListSerializer
        return self.serializer_class


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    filterset_fields = ['product', 'user', 'rating']
    permission_classes = [OwnerOnly, IsAuthenticated]


class FavouriteViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [OwnerOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(user=self.request.user)
        return queryset


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OwnerOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(user=self.request.user,
                                   status=constants.CONFIRMED)
        return queryset
