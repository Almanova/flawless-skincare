import os

import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.getenv('MERCHANT_ID'),
        public_key=os.getenv('PUBLIC_KEY'),
        private_key=os.getenv('PRIVATE_KEY')
    )
)
