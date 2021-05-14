from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Order
from utils import constants
from utils.braintree_util import gateway

import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def braintree_client_token(request):
    return Response({"client_token": gateway.client_token.generate()},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def braintree_checkout(request):
    order = Order.objects.get(id=request.data.get('order'))
    result = gateway.transaction.sale(
        {
            'amount': str(order.total_price),
            'payment_method_nonce': request.data.get('payment_method_nonce'),
            'device_data': request.data.get('device_data'),
            'options': {
                'submit_for_settlement': True
            }
        }
    )
    if result.is_success:
        order.payment.transaction = str(result)
        order.payment.status = constants.SUCCESS
        order.payment.save()
        return Response({'result': str(result)},
                        status=status.HTTP_200_OK)
    order.payment.status = constants.FAILURE
    order.payment.save()
    return Response({'result': 'error occurred'})
