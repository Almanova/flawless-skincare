from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_.models import CustomerProfile, AdminProfile, Brand, User
from auth_.serializers import RegistrationSerializer, \
    UserSerializer, ConfirmationSerializer, CustomerProfileSerializer, \
    AdminProfileSerializer, BrandSerializer, UserUpdateSerializer
from utils.permissions import AccountOwner

import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.register()
    return Response(UserSerializer(user).data,
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def confirm_email(request):
    request.data['uid'] = request.GET.get('uid')
    request.data['token'] = request.GET.get('token')
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if serializer.confirm():
        return Response({'details': 'email confirmed'},
                        status=status.HTTP_200_OK)
    return Response({'details': 'error occurred'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [AccountOwner]


class CustomerProfileAPIView(APIView):
    parser_classes = [MultiPartParser]
    model = CustomerProfile
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer

    def get_object(self, profile_id):
        try:
            return self.queryset.get(id=profile_id)
        except self.model.DoesNotExist as e:
            return Response({'error': str(e)},
                            status=status.HTTP_404_NOT_FOUND)

    def get(self, request, profile_id):
        instance = self.get_object(profile_id)
        serializer = self.serializer_class(instance)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def put(self, request, profile_id):
        instance = self.get_object(profile_id)
        if request.user != instance.user:
            return Response({'error': 'Forbidden'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(instance=instance,
                                           data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class AdminProfileAPIView(CustomerProfileAPIView):
    model = AdminProfile
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer


class BrandDetailsAPIView(CustomerProfileAPIView):
    model = Brand
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
