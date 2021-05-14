from rest_framework import serializers
from .models import Category, Product, ProductImage, \
    CartItem, Review, Favourite, Order, OrderItem
import logging

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('created',
                   'modified',
                   'hidden')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id',
                  'image',
                  'priority')

    def create(self, validated_data):
        validated_data['product'] = self.context.get('product')
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        exclude = ('created',
                   'modified',
                   'hidden',
                   'order_count')
        read_only_fields = ('rating',
                            'images')


class UserAutoAddSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)


class CartItemSerializer(UserAutoAddSerializer):

    class Meta:
        model = CartItem
        fields = ('id',
                  'user',
                  'product',
                  'quantity')
        read_only_fields = ('user', )


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ('id',
                  'product',
                  'quantity')


class ReviewSerializer(UserAutoAddSerializer):
    username = serializers.CharField(max_length=100,
                                     read_only=True,
                                     source='user.username')
    avatar = serializers.FileField(read_only=True,
                                   source='user.customerprofile.avatar')

    class Meta:
        model = Review
        exclude = ('hidden', )
        read_only_fields = ('created',
                            'modified',
                            'user')


class FavouriteSerializer(UserAutoAddSerializer):

    class Meta:
        model = Favourite
        exclude = ('hidden',
                   'modified')
        read_only_fields = ('user', )


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        exclude = ('hidden',
                   'created',
                   'modified',)


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ('hidden',
                   'modified')
        read_only_fields = ('created',
                            'user',
                            'status',
                            'price',
                            'discounted_price',
                            'delivery_price',
                            'total_price',
                            'cashback', )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def get_order_items(self, instance):
        return OrderItemSerializer(instance.order_items.all(),
                                   many=True).data
